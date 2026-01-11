# VerifAI Design System

Complete design specifications for the VerifAI fake news detection platform.

---

## 🎨 Color Palettes

### Dark Theme (Default)
```css
--bg-primary: #0a0a0f;
--bg-secondary: #12121a;
--bg-tertiary: #1a1a24;
--text-primary: #ffffff;
--text-secondary: #a1a1aa;
--text-muted: #71717a;
--accent-primary: #6366f1;      /* Indigo */
--accent-secondary: #818cf8;
--accent-tertiary: #a855f7;     /* Purple */
--border-color: rgba(255, 255, 255, 0.08);
--button-bg: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7);
```

### Light Theme
```css
--bg-primary: #f8fafc;
--bg-secondary: #ffffff;
--bg-tertiary: #f1f5f9;
--text-primary: #0f172a;
--text-secondary: #475569;
--accent-primary: #3b82f6;      /* Blue */
--accent-secondary: #60a5fa;
--button-bg: linear-gradient(135deg, #3b82f6, #2563eb, #1d4ed8);
```

### Forest Theme
```css
--bg-primary: #0d1a0d;
--bg-secondary: #132013;
--bg-tertiary: #1a2b1a;
--text-primary: #e8f5e8;
--text-secondary: #a3d9a3;
--accent-primary: #22c55e;      /* Green */
--accent-secondary: #4ade80;
--button-bg: linear-gradient(135deg, #22c55e, #16a34a, #15803d);
```

### Cream Theme
```css
--bg-primary: #faf8f3;
--bg-secondary: #fff9ed;
--bg-tertiary: #fef3c7;
--text-primary: #451a03;
--text-secondary: #78350f;
--accent-primary: #f59e0b;      /* Amber */
--accent-secondary: #fbbf24;
--button-bg: linear-gradient(135deg, #f59e0b, #d97706, #b45309);
```

### Ocean Theme
```css
--bg-primary: #0c1929;
--bg-secondary: #0f2337;
--bg-tertiary: #132d46;
--text-primary: #e0f2fe;
--text-secondary: #7dd3fc;
--accent-primary: #06b6d4;      /* Cyan */
--accent-secondary: #22d3ee;
--button-bg: linear-gradient(135deg, #06b6d4, #0891b2, #0e7490);
```

---

## 📐 Typography

**Font Family:** Inter (Google Fonts)
```css
font-family: 'Inter', sans-serif;
```

| Element | Size | Weight |
|---------|------|--------|
| Hero Title | 3.5rem | 800 |
| Section Title | 2.5rem | 700 |
| Card Title | 1.25rem | 700 |
| Body Text | 1rem | 400 |
| Small Text | 0.875rem | 400 |
| Muted Text | 0.875rem | 400 |

---

## 🧩 Components

### Navbar
- Fixed position, sticky on scroll
- Backdrop blur effect
- Logo (favicon.png) + brand name clickable → redirects to landing
- Nav links with gradient underline on hover
- Theme dropdown button

### Cards
```css
.card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 30px;
}
.card:hover {
    transform: translateY(-5px);
    border-color: var(--accent-primary);
}
```

### Buttons
```css
/* Primary Button */
.btn-primary {
    background: var(--button-bg);
    color: var(--button-text);
    padding: 12px 32px;
    border-radius: 8px;
}
.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px var(--button-hover-shadow);
}

/* Outline Button */
.btn-outline {
    background: transparent;
    border: 2px solid var(--accent-primary);
    color: var(--accent-primary);
}
```

### FAQ Accordion
- Collapsible items with smooth max-height transition
- Chevron icon rotates 180° when expanded
- Border color changes to accent on hover

### Upload Area
```css
.upload-area {
    border: 2px dashed var(--border-color);
    border-radius: 12px;
    padding: 40px;
    text-align: center;
}
.upload-area:hover {
    border-color: var(--accent-primary);
}
```

---

## 🎬 Animations

### Landing Page
- Logo with expanding rings (3 rings, 0.5s delay each)
- 30 floating particles
- Word-by-word title reveal
- Loading bar animation
- Auto-redirect after 3 seconds

### Floating Background Icons
```css
.floating-icon {
    opacity: 0.15;
    animation: floatIcon 20s ease-in-out infinite;
    filter: drop-shadow(0 0 10px var(--accent-primary));
}
```
Icons: Shield, Checkmark, Document, Eye, Lightbulb, Lock, Search, Brain

### Nav Link Hover
```css
.nav-link::after {
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
    transition: width 0.3s ease;
}
.nav-link:hover::after {
    width: 100%;
}
```

### Theme Transition
```css
* {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
```

---

## 📱 Responsive Breakpoints

| Breakpoint | Width | Changes |
|------------|-------|---------|
| Desktop | > 1024px | Full layout |
| Tablet | 768px - 1024px | 2-column grid |
| Mobile | < 768px | Single column, hamburger menu |

---

## 🔧 Theme Switcher Code

```javascript
function changeTheme(theme) {
    document.body.className = 'theme-' + theme;
    localStorage.setItem('verifai-theme', theme);
}

// On page load
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('verifai-theme') || 'dark';
    document.body.className = 'theme-' + savedTheme;
});
```

---

## 📁 File Reference

| File | Purpose |
|------|---------|
| `index.html` | Landing animation page |
| `home.html` | Main verification UI |
| `about.html` | About & stakeholders |
| `styles.css` | All CSS (themes, components) |
| `scripts.js` | Theme, verification, FAQ logic |
| `favicon.png` | Logo (used in navbar + favicon) |

---

## 🎯 Design Principles

1. **Dark-first design** - Default theme is dark for reduced eye strain
2. **Gradient accents** - All CTAs use theme-specific gradients
3. **Subtle animations** - Micro-interactions enhance UX without distraction
4. **Consistent spacing** - 8px base unit system
5. **Accessible contrast** - All text meets WCAG AA standards
