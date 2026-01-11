/* ============================================
   THEME MANAGEMENT
   ============================================ */

function changeTheme(theme) {
    document.body.className = `theme-${theme}`;

    // Update active button state
    document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.querySelector(`.theme-${theme}-btn`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }

    // Save theme preference
    localStorage.setItem('verifai-theme', theme);
}

// Load saved theme on page load
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('verifai-theme') || 'dark';
    changeTheme(savedTheme);
});

/* ============================================
   IMAGE UPLOAD HANDLING
   ============================================ */

// Initialize upload area if it exists
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');

if (uploadArea && imageInput) {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            imageInput.files = files;
            handleImageUpload({ target: imageInput });
        }
    });
}

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('previewImg').src = e.target.result;
            document.getElementById('imagePreview').classList.remove('hidden');
            document.getElementById('uploadArea').style.display = 'none';
            // Hide any previous results
            document.getElementById('imageResult').classList.add('hidden');
        };
        reader.readAsDataURL(file);
    }
}

function removeImage() {
    // Reset the file input
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.value = '';
    }
    // Hide preview and show upload area
    document.getElementById('imagePreview').classList.add('hidden');
    document.getElementById('uploadArea').style.display = 'block';
    // Clear the preview image
    document.getElementById('previewImg').src = '';
    // Hide any previous results
    document.getElementById('imageResult').classList.add('hidden');
}

/* ============================================
   TEXT VERIFICATION
   ============================================ */

function verifyText() {
    const text = document.getElementById('textInput').value;
    if (!text.trim()) {
        alert('Please enter some text to analyze');
        return;
    }

    // Simulate AI analysis with random scoring
    const resultDiv = document.getElementById('textResult');
    const score = Math.floor(Math.random() * 100);
    const isFake = score < 60;

    resultDiv.innerHTML = `
        <div style="text-align: center;">
            <div class="score-circle">
                <span style="color: ${score >= 60 ? '#4ade80' : '#f87171'};">${score}%</span>
            </div>
            <h3 class="text-xl font-bold mb-2" style="color: var(--text-primary);">Credibility Score</h3>
            <div class="result-badge ${isFake ? 'badge-fake' : 'badge-real'}">
                ${isFake ? '⚠️ Potentially Fake News' : '✅ Likely Credible'}
            </div>
            <p class="mt-4" style="color: var(--text-muted);">
                ${isFake
            ? 'This content shows signs of misinformation. Cross-reference with trusted sources.'
            : 'This content appears credible based on our analysis. Always verify important information.'}
            </p>
        </div>
    `;
    resultDiv.classList.remove('hidden');

    // Smooth scroll to results
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ============================================
   IMAGE VERIFICATION
   ============================================ */

function verifyImage() {
    const resultDiv = document.getElementById('imageResult');
    const score = Math.floor(Math.random() * 100);
    const isManipulated = score < 65;

    resultDiv.innerHTML = `
        <div style="text-align: center;">
            <div class="score-circle">
                <span style="color: ${score >= 65 ? '#4ade80' : '#f87171'};">${score}%</span>
            </div>
            <h3 class="text-xl font-bold mb-2" style="color: var(--text-primary);">Authenticity Score</h3>
            <div class="result-badge ${isManipulated ? 'badge-fake' : 'badge-real'}">
                ${isManipulated ? '⚠️ Possible Manipulation Detected' : '✅ Appears Authentic'}
            </div>
            <p class="mt-4" style="color: var(--text-muted);">
                ${isManipulated
            ? 'AI detected potential image manipulation. Verify the source before sharing.'
            : 'No significant manipulation detected. Image appears to be authentic.'}
            </p>
        </div>
    `;
    resultDiv.classList.remove('hidden');

    // Smooth scroll to results
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ============================================
   FAQ TOGGLE
   ============================================ */

function toggleFAQ(element) {
    const faqItem = element.closest('.faq-item');
    const isActive = faqItem.classList.contains('active');

    // Close all FAQ items
    document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('active');
    });

    // Toggle current item
    if (!isActive) {
        faqItem.classList.add('active');
    }
}

// Initialize FAQ items
document.addEventListener('DOMContentLoaded', () => {
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(question => {
        question.addEventListener('click', function () {
            toggleFAQ(this);
        });
    });
});

/* ============================================
   MOBILE MENU TOGGLE
   ============================================ */

function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    if (navLinks) {
        navLinks.classList.toggle('active');
    }
    if (mobileMenuBtn) {
        mobileMenuBtn.classList.toggle('active');
    }
}
