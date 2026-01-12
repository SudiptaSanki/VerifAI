# VerifAI - Fake News Detection Platform

AI-powered platform for detecting and classifying fake news using **NLP, BERT, and Text Classification**.

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 🚨 **Fake News Alerts** | Real-time detection with clear verdicts |
| 📊 **Credibility Scoring** | 0-100% score based on multi-model analysis |
| 🛡️ **Reduced Misinformation** | Combines ML + BERT + LLM + Web verification |
| 🖼️ **Image Analysis** | OCR text extraction + visual manipulation detection |

---

## 📁 Files You Need

### **Required Files (Must Download)**

| File | Size | Description |
|------|------|-------------|
| `text_detection.py` | 6 KB | Text-based fake news detection API |
| `image_detection.py` | 13 KB | Image-based fake news detection API |
| `Fake.csv` | ~60 MB | Fake news training dataset |
| `True.csv` | ~51 MB | Real news training dataset |
| `distilbert_model/` | ~250 MB | Pre-trained DistilBERT model folder |

### **Auto-Generated Files (Created on first run)**

| File | Description |
|------|-------------|
| `model.pkl` | Trained Logistic Regression model |
| `vectorizer.pkl` | TF-IDF vectorizer |

### **Frontend Files (Optional - for web interface)**

| File | Description |
|------|-------------|
| `index.html` | Landing page with animation |
| `home.html` | Main verification interface |
| `about.html` | About page |
| `styles.css` | Theme styles (5 themes) |
| `scripts.js` | Frontend JavaScript |
| `favicon.png` | Site icon |

---

## 🔑 API Keys Required

You need to set up your own API keys in the Python files:

### `text_detection.py` (Line 31)
```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

### `image_detection.py` (Line 47)
```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

### How to Get Gemini API Key:
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with Google account
3. Click "Get API Key" → "Create API Key"
4. Copy and paste into the files above

---

## 🛠️ Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/verifai-news.git
cd verifai-news
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install flask flask-cors pandas scikit-learn torch transformers google-generativeai ddgs easyocr pillow
```

### Step 4: Download Required Data

Make sure you have these files in your project folder:
- `Fake.csv` - [Download from Kaggle](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
- `True.csv` - Same dataset as above
- `distilbert_model/` - Pre-trained DistilBERT model folder

---

## 🚀 How to Run

### Run Text Detection API (Port 5000)
```bash
python text_detection.py
```

### Run Image Detection API (Port 5001)
```bash
python image_detection.py
```

> **Note:** On first run, the ML model will be trained automatically (takes ~1-2 minutes).

---

## 📡 API Documentation

### Text Detection API

**Endpoint:** `POST http://localhost:5000/check`

**Request:**
```json
{
  "text": "Breaking: Scientists discover water on Mars!"
}
```

**Response:**
```json
{
  "credibility": 75,
  "verdict": "LIKELY REAL",
  "ml_score": 0.82,
  "bert_score": 0.71,
  "llm_score": 0.68,
  "web_score": 0.5
}
```

---

### Image Detection API

**Endpoint:** `POST http://localhost:5001/check-image`

**Request (Base64):**
```json
{
  "image": "data:image/png;base64,iVBORw0KGgo..."
}
```

**Request (File Upload):**
```bash
curl -X POST -F "image=@path/to/image.png" http://localhost:5001/check-image
```

**Response:**
```json
{
  "credibility": 65,
  "verdict": "UNVERIFIABLE",
  "alert": "⚠️ Unable to verify - Exercise caution",
  "extracted_text": "Breaking news headline from image...",
  "ml_score": 0.72,
  "bert_score": 0.68,
  "llm_score": 0.55,
  "web_score": 0.3,
  "image_manipulation_score": 0.2,
  "concerns": "None detected"
}
```

---

## 📊 Verdict Types

| Verdict | Credibility | Meaning |
|---------|-------------|---------|
| ✅ `REAL` | 85%+ | Verified by trusted sources |
| ✅ `LIKELY REAL` | 65-84% | Appears credible |
| ⚠️ `UNVERIFIABLE` | 40-64% | Cannot confirm |
| ⚠️ `SUSPICIOUS` | 20-39% | Signs of manipulation |
| 🚨 `FAKE` | 0-19% | High manipulation detected |

---

## 🧠 Technology Stack

| Component | Technology |
|-----------|------------|
| **NLP** | TF-IDF Vectorization, Text Preprocessing |
| **BERT** | DistilBERT for Sequence Classification |
| **ML** | Scikit-learn Logistic Regression |
| **LLM** | Google Gemini 1.5 Flash |
| **OCR** | EasyOCR (for image text extraction) |
| **Web** | Flask REST API |

---

## 🎨 Frontend Theme System

| Theme | Background | Accent |
|-------|-----------|--------|
| Dark (Default) | `#0a0a0f` | Indigo |
| Light | `#f8fafc` | Blue |
| Forest | `#0d1a0d` | Green |
| Cream | `#faf8f3` | Amber |
| Ocean | `#0c1929` | Cyan |

---

## 📋 Troubleshooting

### `ModuleNotFoundError: No module named 'torch'`
```bash
pip install torch
```

### `ModuleNotFoundError: No module named 'transformers'`
```bash
pip install transformers
```

### `Model files not found`
Make sure `distilbert_model/` folder exists with:
- `config.json`
- `pytorch_model.bin` or `model.safetensors`
- `vocab.txt`

### `API Key Error`
Replace placeholder API keys with your actual Gemini API key.

---

**Live URL:** `https://verifai-news.web.app`

---

## 📞 Support

For issues or contributions, please open a GitHub Issue.

---

## 📄 License

MIT License - Feel free to use and modify!

