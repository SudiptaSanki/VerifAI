import re
import os
import pickle
import torch
import pandas as pd

from flask import Flask, request, jsonify
from flask_cors import CORS
from ddgs import DDGS
import google.generativeai as genai

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
GEMINI_API_KEY = "AIzaSyAVH2lB_sryUv_pH5bm5UrLs7nX6BCI3PA"
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel("gemini-1.5-flash")

TRUSTED_DOMAINS = [
    "bbc.com", "reuters.com", "apnews.com",
    "nytimes.com", "theguardian.com",
    "cnn.com", "ndtv.com", "gov"
]

app = Flask(__name__)
CORS(app)

# =====================================================
# HELPERS
# =====================================================

def clean_text(text):
    text = text.lower()
    return re.sub(r"[^a-z ]", "", text)

def is_factual_claim(text):
    keywords = [
        "is", "was", "announced", "confirmed", "became",
        "won", "launched", "approved", "reported"
    ]
    return any(k in text.lower() for k in keywords)

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
# LOAD DISTILBERT (STABLE)
# =====================================================

tokenizer = DistilBertTokenizer.from_pretrained(
    MODEL_DIR, local_files_only=True
)
bert_model = DistilBertForSequenceClassification.from_pretrained(
    MODEL_DIR, local_files_only=True
)
bert_model.eval()

# =====================================================
# SCORES
# =====================================================

def ml_score(text):
    vec = vectorizer.transform([clean_text(text)])
    return model.predict_proba(vec)[0][1]

def bert_score(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = bert_model(**inputs).logits
        probs = torch.softmax(logits, dim=1)
    return probs[0][1].item()

def llm_score(text):
    prompt = f"""
Evaluate the factual plausibility of the following claim.

Rules:
- Impossible or false → CONFIDENCE: 0
- Clearly true → CONFIDENCE: 1
- Uncertain → CONFIDENCE: 0.5

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
# FINAL ANALYSIS (FIXED LOGIC)
# =====================================================

def analyze_news(text):
    if not is_factual_claim(text):
        return {
            "credibility": 0,
            "verdict": "NOT A FACTUAL CLAIM",
            "ml_score": 0,
            "bert_score": 0,
            "llm_score": 0,
            "web_score": 0
        }

    ml = ml_score(text)
    bert = bert_score(text)
    llm = llm_score(text)
    web = web_score(text)

    # HARD RULES
    if llm < 0.2:
        verdict = "FAKE"
        credibility = 10
    elif web >= 0.8:
        verdict = "REAL"
        credibility = 85
    elif bert > 0.6 and llm > 0.6:
        verdict = "LIKELY REAL"
        credibility = 65
    else:
        verdict = "UNVERIFIABLE"
        credibility = 40

    return {
        "credibility": credibility,
        "verdict": verdict,
        "ml_score": round(ml, 3),
        "bert_score": round(bert, 3),
        "llm_score": round(llm, 3),
        "web_score": round(web, 3)
    }

# =====================================================
# API
# =====================================================

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "text required"}), 400
    return jsonify(analyze_news(data["text"]))

# =====================================================
# START
# =====================================================

if __name__ == "__main__":
    if not os.path.exists(ML_MODEL_PATH):
        model, vectorizer = train_ml()
    else:
        model, vectorizer = load_ml()

    app.run(port=5000, debug=True)
