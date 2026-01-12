# VerifAI Design System

Complete design specifications for the VerifAI Fake News Detection Platform.

---

## 🎨 Color Palettes

### Dark Theme (Default)
| Token | Value | Usage |
|-------|-------|-------|
| `--bg-primary` | `#0a0a0f` | Main background |
| `--bg-secondary` | `#12121a` | Cards, sections |
| `--text-primary` | `#ffffff` | Headings |
| `--text-secondary` | `#a1a1aa` | Body text |
| `--accent` | `#6366f1` | Indigo - buttons, links |
| `--accent-glow` | `rgba(99, 102, 241, 0.3)` | Glow effects |

### Light Theme
| Token | Value |
|-------|-------|
| `--bg-primary` | `#f8fafc` |
| `--bg-secondary` | `#ffffff` |
| `--text-primary` | `#1e293b` |
| `--accent` | `#3b82f6` |

### Forest Theme
| Token | Value |
|-------|-------|
| `--bg-primary` | `#0d1a0d` |
| `--accent` | `#22c55e` |

### Cream Theme
| Token | Value |
|-------|-------|
| `--bg-primary` | `#faf8f3` |
| `--accent` | `#f59e0b` |

### Ocean Theme
| Token | Value |
|-------|-------|
| `--bg-primary` | `#0c1929` |
| `--accent` | `#06b6d4` |

---

## 📐 Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| H1 | Inter | 3rem | 700 |
| H2 | Inter | 2rem | 600 |
| H3 | Inter | 1.5rem | 600 |
| Body | Inter | 1rem | 400 |
| Small | Inter | 0.875rem | 400 |

---

## 🧩 Components

### Buttons
```css
.btn-primary {
  background: var(--accent);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px var(--accent-glow);
}
```

### Cards
```css
.card {
  background: var(--bg-secondary);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

### Input Fields
```css
.input {
  background: var(--bg-primary);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 12px 16px;
  color: var(--text-primary);
}
```

---

## 📱 Breakpoints

| Breakpoint | Width | Target |
|------------|-------|--------|
| Mobile | < 768px | Phones |
| Tablet | 768px - 1024px | Tablets |
| Desktop | > 1024px | Laptops, Desktops |

---

## ⚡ Animations

### Fade In
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Pulse
```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
```

### Hamburger to X
```css
.hamburger.active span:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}
.hamburger.active span:nth-child(2) {
  opacity: 0;
}
.hamburger.active span:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -7px);
}
```

---

## 🔌 Backend API Integration

### Text Verification
| Property | Value |
|----------|-------|
| Endpoint | `POST /check` |
| Port | 5000 |
| File | `text_detection.py` |

### Image Verification
| Property | Value |
|----------|-------|
| Endpoint | `POST /check-image` |
| Port | 5001 |
| File | `image_detection.py` |

---

## 📊 Credibility Score Display

| Score Range | Color | Label |
|-------------|-------|-------|
| 80-100% | `#22c55e` (Green) | Verified |
| 60-79% | `#84cc16` (Lime) | Likely Real |
| 40-59% | `#eab308` (Yellow) | Uncertain |
| 20-39% | `#f97316` (Orange) | Suspicious |
| 0-19% | `#ef4444` (Red) | Fake |

---

## 🗂️ File Structure

```
verifai-news/
├── Frontend/
│   ├── index.html          # Landing animation
│   ├── home.html           # Main interface
│   ├── about.html          # About page
│   ├── styles.css          # All styles
│   ├── scripts.js          # Frontend logic
│   └── favicon.png         # Icon
│
├── Backend/
│   ├── text_detection.py   # Text API (port 5000)
│   ├── image_detection.py  # Image API (port 5001)
│   ├── model.pkl           # Trained ML model
│   └── vectorizer.pkl      # TF-IDF vectorizer
│
├── Data/
│   ├── Fake.csv            # Fake news dataset
│   ├── True.csv            # Real news dataset
│   └── distilbert_model/   # BERT model files
│
└── Config/
    ├── firebase.json       # Firebase config
    ├── .firebaserc         # Firebase project
    ├── README.md           # User guide
    └── DESIGN_SYSTEM.md    # This file
```

---

## 🛠️ Tech Stack Summary

| Layer | Technology |
|-------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| ML/AI | Scikit-learn, PyTorch, Transformers |
| NLP | TF-IDF, DistilBERT |
| LLM | Google Gemini 1.5 Flash |
| OCR | EasyOCR |
| Hosting | Firebase |
