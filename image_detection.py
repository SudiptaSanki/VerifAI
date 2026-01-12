"""
🖼️ IMAGE-BASED FAKE NEWS DETECTION
===================================
Uses: NLP, BERT, Text Classification
Outcomes: Fake News Alerts, Credibility Scoring, Reduced Misinformation

This module extracts text from images using OCR, then applies
the same BERT + ML + LLM pipeline for fake news detection.
"""

import re
import os
import io
import base64
import pickle
import torch
import pandas as pd

from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
from ddgs import DDGS
import google.generativeai as genai

# OCR
import easyocr

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification
)

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "distilbert_model")

ML_MODEL_PATH = "model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

# 🔑 GEMINI API KEY
GEMINI_API_KEY = "Enter Your API key HERE"
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel("gemini-1.5-flash")

TRUSTED_DOMAINS = [
    "bbc.com", "reuters.com", "apnews.com",
    "nytimes.com", "theguardian.com",
    "cnn.com", "ndtv.com", "gov"
]

app = Flask(__name__)
CORS(app)

# Initialize EasyOCR reader (supports multiple languages)
ocr_reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())

# =====================================================
# HELPERS
# =====================================================

def clean_text(text):
    text = text.lower()
    return re.sub(r"[^a-z ]+", " ", text)

def is_factual_claim(text):
    keywords = [
        "is", "was", "announced", "confirmed", "became",
        "won", "launched", "approved", "reported", "said",
        "breaking", "urgent", "exclusive", "official"
    ]
    return any(k in text.lower() for k in keywords)

def decode_base64_image(base64_string):
    """Decode base64 string to PIL Image"""
    # Remove data URL prefix if present
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    
    image_data = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(image_data))

# =====================================================
# OCR - TEXT EXTRACTION FROM IMAGE
# =====================================================

def extract_text_from_image(image):
    """
    Extract text from image using EasyOCR.
    Supports PIL Image, file path, or numpy array.
    """
    try:
        if isinstance(image, str):
            # File path
            results = ocr_reader.readtext(image)
        elif isinstance(image, Image.Image):
            # PIL Image - convert to numpy
            import numpy as np
            img_array = np.array(image)
            results = ocr_reader.readtext(img_array)
        else:
            # Assume numpy array
            results = ocr_reader.readtext(image)
        
        # Combine all detected text
        extracted_text = " ".join([result[1] for result in results])
        return extracted_text.strip()
    
    except Exception as e:
        print(f"[OCR ERROR]: {e}")
        return ""

# =====================================================
# TRAIN / LOAD ML
# =====================================================

def train_ml():
    fake = pd.read_csv("Fake.csv")
    real = pd.read_csv("True.csv")

    fake["label"] = 0
    real["label"] = 1

    df = pd.concat([fake, real]).sample(frac=1).reset_index(drop=True)
    df["text"] = df["text"].apply(clean_text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_df=0.7,
        ngram_range=(1, 2)
    )

    X = vectorizer.fit_transform(df["text"])
    y = df["label"]

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    pickle.dump(model, open(ML_MODEL_PATH, "wb"))
    pickle.dump(vectorizer, open(VECTORIZER_PATH, "wb"))

    return model, vectorizer

def load_ml():
    return (
        pickle.load(open(ML_MODEL_PATH, "rb")),
        pickle.load(open(VECTORIZER_PATH, "rb"))
    )

# =====================================================
# LOAD DISTILBERT
# =====================================================

tokenizer = DistilBertTokenizer.from_pretrained(
    MODEL_DIR, local_files_only=True
)
bert_model = DistilBertForSequenceClassification.from_pretrained(
    MODEL_DIR, local_files_only=True
)
bert_model.eval()

# =====================================================
# SCORING FUNCTIONS
# =====================================================

def ml_score(text):
    vec = vectorizer.transform([clean_text(text)])
    return model.predict_proba(vec)[0][1]

def bert_score(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        logits = bert_model(**inputs).logits
        probs = torch.softmax(logits, dim=1)
    return probs[0][1].item()

def llm_score(text):
    prompt = f"""
Evaluate the factual plausibility of the following claim extracted from an image.

Rules:
- Clearly false or impossible → CONFIDENCE: 0
- Clearly true and verifiable → CONFIDENCE: 1
- Uncertain or unverifiable → CONFIDENCE: 0.5

Respond ONLY as:
CONFIDENCE: <number>

Claim:
{text}
"""
    try:
        response = gemini.generate_content(
            prompt,
            generation_config={"temperature": 0}
        )
        match = re.search(r"CONFIDENCE:\s*([0-9.]+)", response.text)
        return float(match.group(1)) if match else 0.5
    except:
        return 0.5

def llm_image_analysis(image):
    """
    Use Gemini Vision to directly analyze the image for
    signs of manipulation, fake news patterns, etc.
    """
    try:
        prompt = """
Analyze this image for signs of misinformation or manipulation.

Check for:
1. Sensationalist text overlays
2. Misleading statistics or claims
3. Signs of image manipulation
4. Fake news visual patterns

Respond ONLY as:
MANIPULATION_SCORE: <0 to 1, where 0 is genuine and 1 is fake>
CONCERNS: <brief description or "None">
"""
        response = gemini.generate_content([prompt, image])
        
        # Parse manipulation score
        match = re.search(r"MANIPULATION_SCORE:\s*([0-9.]+)", response.text)
        manipulation_score = float(match.group(1)) if match else 0.5
        
        # Parse concerns
        concerns_match = re.search(r"CONCERNS:\s*(.+)", response.text, re.IGNORECASE)
        concerns = concerns_match.group(1).strip() if concerns_match else "Unable to analyze"
        
        return manipulation_score, concerns
    
    except Exception as e:
        print(f"[IMAGE ANALYSIS ERROR]: {e}")
        return 0.5, "Analysis failed"

def web_score(text):
    query = " ".join(text.split()[:8])
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=8))
    except:
        return 0.0

    hits = sum(
        1 for r in results
        if any(d in r.get("href", "") for d in TRUSTED_DOMAINS)
    )
    return min(hits / 2, 1.0)

# =====================================================
# MAIN ANALYSIS
# =====================================================

def analyze_image(image_input, is_base64=False):
    """
    Complete image analysis pipeline:
    1. Extract text via OCR
    2. Analyze with BERT/ML/LLM
    3. Direct image analysis with Gemini Vision
    4. Return comprehensive credibility report
    """
    
    # Step 1: Handle image input
    if is_base64:
        image = decode_base64_image(image_input)
    elif isinstance(image_input, str) and os.path.exists(image_input):
        image = Image.open(image_input)
    else:
        image = image_input
    
    # Step 2: Extract text from image
    extracted_text = extract_text_from_image(image)
    
    if not extracted_text:
        return {
            "credibility": 0,
            "verdict": "NO TEXT DETECTED",
            "alert": "⚠️ No readable text found in image",
            "extracted_text": "",
            "ml_score": 0,
            "bert_score": 0,
            "llm_score": 0,
            "web_score": 0,
            "image_manipulation_score": 0,
            "concerns": "No text to analyze"
        }
    
    # Step 3: Check if extracted text contains a factual claim
    if not is_factual_claim(extracted_text):
        # Still do image analysis
        manipulation_score, concerns = llm_image_analysis(image)
        
        return {
            "credibility": int((1 - manipulation_score) * 100),
            "verdict": "NOT A FACTUAL CLAIM",
            "alert": "ℹ️ Image does not contain verifiable claims",
            "extracted_text": extracted_text,
            "ml_score": 0,
            "bert_score": 0,
            "llm_score": 0,
            "web_score": 0,
            "image_manipulation_score": round(manipulation_score, 3),
            "concerns": concerns
        }
    
    # Step 4: Run full analysis pipeline
    ml = ml_score(extracted_text)
    bert = bert_score(extracted_text)
    llm = llm_score(extracted_text)
    web = web_score(extracted_text)
    manipulation_score, concerns = llm_image_analysis(image)
    
    # Step 5: Calculate final credibility
    # Weighted combination: BERT (25%), ML (20%), LLM (25%), Web (15%), Image (15%)
    text_credibility = (0.25 * bert) + (0.20 * ml) + (0.25 * llm) + (0.15 * web)
    image_credibility = 1 - manipulation_score
    
    final_credibility = (0.85 * text_credibility) + (0.15 * image_credibility)
    credibility_percent = int(final_credibility * 100)
    
    # Step 6: Determine verdict and alert
    if llm < 0.2 or manipulation_score > 0.8:
        verdict = "FAKE"
        alert = "🚨 FAKE NEWS ALERT - High manipulation detected!"
        credibility_percent = min(credibility_percent, 15)
    elif web >= 0.8 and bert > 0.6:
        verdict = "REAL"
        alert = "✅ VERIFIED - Content appears credible"
    elif bert > 0.6 and llm > 0.6:
        verdict = "LIKELY REAL"
        alert = "✅ Content appears mostly credible"
    elif manipulation_score > 0.5:
        verdict = "SUSPICIOUS"
        alert = "⚠️ CAUTION - Image shows signs of manipulation"
        credibility_percent = min(credibility_percent, 40)
    else:
        verdict = "UNVERIFIABLE"
        alert = "⚠️ Unable to verify - Exercise caution"
    
    return {
        "credibility": credibility_percent,
        "verdict": verdict,
        "alert": alert,
        "extracted_text": extracted_text,
        "ml_score": round(ml, 3),
        "bert_score": round(bert, 3),
        "llm_score": round(llm, 3),
        "web_score": round(web, 3),
        "image_manipulation_score": round(manipulation_score, 3),
        "concerns": concerns
    }

# =====================================================
# API ENDPOINTS
# =====================================================

@app.route("/check-image", methods=["POST"])
def check_image():
    """
    Endpoint for image-based fake news detection.
    
    Accepts:
    - JSON with 'image' field containing base64 encoded image
    - Form data with 'image' file upload
    """
    
    try:
        # Check for base64 image in JSON
        if request.is_json:
            data = request.json
            if not data or "image" not in data:
                return jsonify({"error": "image field required"}), 400
            
            result = analyze_image(data["image"], is_base64=True)
            return jsonify(result)
        
        # Check for file upload
        if "image" in request.files:
            file = request.files["image"]
            image = Image.open(file.stream)
            result = analyze_image(image)
            return jsonify(result)
        
        return jsonify({"error": "No image provided"}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "Image Fake News Detection",
        "features": ["OCR", "BERT", "NLP", "Text Classification", "Vision AI"]
    })

# =====================================================
# START
# =====================================================

if __name__ == "__main__":
    print("🖼️ Image Fake News Detection API")
    print("=" * 40)
    
    if not os.path.exists(ML_MODEL_PATH):
        print("📚 Training ML model...")
        model, vectorizer = train_ml()
    else:
        print("📦 Loading ML model...")
        model, vectorizer = load_ml()
    
    print("✅ Models loaded successfully!")
    print("🚀 Starting server on port 5001...")
    print("=" * 40)
    
    app.run(port=5001, debug=True)

