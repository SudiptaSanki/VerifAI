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
async function verifyText() {
    const text = document.getElementById("textInput").value.trim();
    const resultDiv = document.getElementById("textResult");

    if (!text) {
        alert("Please enter some text to analyze.");
        return;
    }

    // Show loading state
    resultDiv.classList.remove("hidden");
    resultDiv.innerHTML = `
        <div style="text-align:center; padding:20px;">
            <p style="opacity:0.8;">🔍 Analyzing news credibility...</p>
        </div>
    `;

    try {
        const response = await fetch("http://127.0.0.1:5000/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!response.ok) {
            resultDiv.innerHTML = `
                <p style="color:#f87171;">${data.error || "Server error"}</p>
            `;
            return;
        }

        // Decide color based on verdict
        let color, icon;
        if (data.verdict === "REAL") {
            color = "#4ade80";
            icon = "✅";
        } else if (data.verdict === "FAKE") {
            color = "#f87171";
            icon = "🚨";
        } else {
            color = "#facc15";
            icon = "⚠️";
        }

        resultDiv.innerHTML = `
            <div style="text-align:center;">
                <div class="score-circle">
                    <span style="color:${color};">
                        ${data.credibility}%
                    </span>
                </div>

                <h3 class="text-xl font-bold mt-2" style="color:${color};">
                    ${icon} ${data.verdict}
                </h3>

                <div style="margin-top:12px; font-size:14px; opacity:0.85;">
                    <p>ML Score: ${data.ml_score}</p>
                    <p>BERT Score: ${data.bert_score}</p>
                    <p>LLM Score: ${data.llm_score}</p>
                    <p>Web Score: ${data.web_score}</p>
                </div>
            </div>
        `;

        // Smooth scroll to result
        resultDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });

    } catch (err) {
        console.error(err);
        resultDiv.innerHTML = `
            <p style="color:#f87171;">
                🚫 Backend not reachable. Is the server running?
            </p>
        `;
    }
}


/* ============================================
   IMAGE VERIFICATION
   ============================================ */

async function verifyImage() {
    const resultDiv = document.getElementById('imageResult');
    const previewImg = document.getElementById('previewImg');
    
    if (!previewImg || !previewImg.src) {
        alert("Please upload an image first.");
        return;
    }

    // Show loading state
    resultDiv.classList.remove('hidden');
    resultDiv.innerHTML = `
        <div style="text-align:center; padding:20px;">
            <p style="opacity:0.8;">🔍 Analyzing image for fake news...</p>
        </div>
    `;

    try {
        const response = await fetch("http://127.0.0.1:5001/check-image", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ image: previewImg.src })
        });

        const data = await response.json();

        if (!response.ok) {
            resultDiv.innerHTML = `
                <p style="color:#f87171;">${data.error || "Server error"}</p>
            `;
            return;
        }

        // Decide color based on verdict
        let color, icon;
        if (data.verdict === "REAL" || data.verdict === "LIKELY REAL") {
            color = "#4ade80";
            icon = "✅";
        } else if (data.verdict === "FAKE") {
            color = "#f87171";
            icon = "🚨";
        } else if (data.verdict === "SUSPICIOUS") {
            color = "#fb923c";
            icon = "⚠️";
        } else {
            color = "#facc15";
            icon = "⚠️";
        }

        resultDiv.innerHTML = `
            <div style="text-align: center;">
                <div class="score-circle">
                    <span style="color: ${color};">${data.credibility}%</span>
                </div>
                <h3 class="text-xl font-bold mt-2" style="color: ${color};">
                    ${icon} ${data.verdict}
                </h3>
                <p class="mt-2" style="color: var(--text-muted); font-size: 14px;">
                    ${data.alert}
                </p>
                
                ${data.extracted_text ? `
                <div style="margin-top: 16px; padding: 12px; background: rgba(0,0,0,0.2); border-radius: 8px; text-align: left;">
                    <p style="font-size: 12px; opacity: 0.7; margin-bottom: 4px;">📝 Extracted Text:</p>
                    <p style="font-size: 13px; font-style: italic;">"${data.extracted_text.substring(0, 150)}${data.extracted_text.length > 150 ? '...' : ''}"</p>
                </div>
                ` : ''}
                
                <div style="margin-top: 12px; font-size: 14px; opacity: 0.85;">
                    <p>ML Score: ${data.ml_score}</p>
                    <p>BERT Score: ${data.bert_score}</p>
                    <p>LLM Score: ${data.llm_score}</p>
                    <p>Web Score: ${data.web_score}</p>
                    <p>Manipulation: ${data.image_manipulation_score}</p>
                </div>
                
                ${data.concerns && data.concerns !== "None" ? `
                <p class="mt-3" style="color: #fb923c; font-size: 13px;">
                    ⚠️ ${data.concerns}
                </p>
                ` : ''}
            </div>
        `;

        // Smooth scroll to results
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    } catch (err) {
        console.error(err);
        resultDiv.innerHTML = `
            <p style="color:#f87171;">
                🚫 Backend not reachable. Is the image detection server running on port 5001?
            </p>
        `;
    }
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
