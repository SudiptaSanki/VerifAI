# VerifAI - Fake News Detection Platform

AI-powered platform for detecting and classifying fake news using content analysis and source verification.

## 🚀 Quick Start

```bash
# Install Firebase CLI (if not installed)
npm install -g firebase-tools

# Login to Firebase
firebase login

# Deploy to production
firebase deploy
```

## 📁 Project Structure

```
NEWS/
├── index.html          # Landing page with animation (auto-redirects to home)
├── home.html           # Main verification interface
├── about.html          # About page with stakeholders & technology info
├── styles.css          # Global styles with 5 theme palettes
├── scripts.js          # Theme management, verification logic, FAQ toggle
├── favicon.png         # Site favicon/logo
├── firebase.json       # Firebase hosting configuration
├── .firebaserc         # Firebase project settings (verifai-news)
├── DESIGN_SYSTEM.md    # Complete design specifications
└── README.md           # This file
```

## 🎨 Theme System

| Theme | Background | Accent | Use Case |
|-------|-----------|--------|----------|
| Dark | `#0a0a0f` | `#6366f1` (Indigo) | Default |
| Light | `#f8fafc` | `#3b82f6` (Blue) | Day mode |
| Forest | `#0d1a0d` | `#22c55e` (Green) | Nature theme |
| Cream | `#faf8f3` | `#f59e0b` (Amber) | Warm theme |
| Ocean | `#0c1929` | `#06b6d4` (Cyan) | Cool theme |

## 🔌 Backend Integration Points

### Text Verification API
```javascript
// Location: scripts.js → verifyText()
// Current: Mock implementation
// Backend endpoint needed: POST /api/verify/text

Request:
{
  "content": "Article text to verify...",
  "type": "text"
}

Response:
{
  "credibilityScore": 85,
  "verdict": "likely_real" | "likely_fake" | "uncertain",
  "confidence": 0.85,
  "sources": ["source1.com", "source2.com"],
  "analysisDetails": {
    "languagePatterns": {...},
    "sourceCredibility": {...},
    "factCheck": {...}
  }
}
```

### Image Verification API
```javascript
// Location: scripts.js → verifyImage()
// Current: Mock implementation
// Backend endpoint needed: POST /api/verify/image

Request:
{
  "image": "base64_encoded_image_data",
  "type": "image"
}

Response:
{
  "isAuthentic": true | false,
  "manipulationScore": 15,
  "deepfakeConfidence": 0.05,
  "analysisDetails": {
    "metadataCheck": {...},
    "forensicAnalysis": {...},
    "reverseImageSearch": {...}
  }
}
```

## 🛠️ Key Functions to Replace

| Function | File | Line | Purpose |
|----------|------|------|---------|
| `verifyText()` | scripts.js | ~45 | Replace mock with API call |
| `verifyImage()` | scripts.js | ~75 | Replace mock with API call |
| `displayTextResult()` | scripts.js | ~60 | Update to parse API response |
| `displayImageResult()` | scripts.js | ~90 | Update to parse API response |

## 📱 Pages Overview

### Landing Page (`index.html`)
- Animated logo with expanding rings
- Floating particles background
- Auto-redirect to home.html after 3 seconds

### Home Page (`home.html`)
- Text verification card (textarea input)
- Image verification card (drag & drop upload)
- "How It Works" animated demo (3 steps)
- Feature highlights section
- FAQ accordion

### About Page (`about.html`)
- Mission statement
- Stakeholder information (Media, Government, Social Platforms)
- Expected outcomes
- Statistics display
- Technology stack overview

## 🔧 Firebase Configuration

**Project ID:** `verifai-news`

```json
// firebase.json
{
  "hosting": {
    "public": ".",
    "ignore": ["firebase.json", "**/.*", "DESIGN_SYSTEM.md"]
  }
}
```

## 📋 Backend Team Checklist

- [ ] Set up API server (Node.js/Python/etc.)
- [ ] Implement `/api/verify/text` endpoint
- [ ] Implement `/api/verify/image` endpoint
- [ ] Connect AI/ML models for analysis
- [ ] Set up database for logging (optional)
- [ ] Configure CORS for frontend domain
- [ ] Update `scripts.js` with real API endpoints
- [ ] Add loading states during API calls
- [ ] Implement error handling for failed requests

## 🌐 Deployment

**Production URL:** `https://verifai-news.web.app`

```bash
# Preview locally
firebase serve

# Deploy to production
firebase deploy

# Deploy only hosting
firebase deploy --only hosting
```

## 📞 Contact

For frontend questions, refer to `DESIGN_SYSTEM.md` for complete specifications.
