const pdfFile = document.getElementById('pdfFile');
const uploadStatus = document.getElementById('uploadStatus');
const questionInput = document.getElementById('questionInput');
const submitBtn = document.getElementById('submitBtn');
const answerText = document.getElementById('answerText');

// Determine API URL based on environment
// For local development, it assumes Backend is running on port 8000
// In production via Render, it might need to point to the deployed backend URL
const API_URL = '';

pdfFile.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) {
        uploadStatus.textContent = 'No file chosen';
        uploadStatus.style.color = 'var(--text-secondary)';
        return;
    }

    uploadStatus.textContent = 'Uploading...';
    uploadStatus.style.color = 'var(--text-secondary)';
    
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        if (response.ok) {
            uploadStatus.textContent = 'File uploaded successfully.';
            uploadStatus.style.color = '#10b981'; // Green for success
        } else {
            uploadStatus.textContent = 'Error: ' + data.error;
            uploadStatus.style.color = '#ef4444'; // Red for error
        }
    } catch (err) {
        uploadStatus.textContent = 'Failed to upload.';
        uploadStatus.style.color = '#ef4444';
    }
});

submitBtn.addEventListener('click', async () => {
    const question = questionInput.value.trim();
    if (!question) return;

    submitBtn.disabled = true;
    submitBtn.textContent = 'Thinking...';
    
    answerText.textContent = 'Generating answer...';
    answerText.className = 'placeholder-text';

    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        if (response.ok && data.answer) {
            // Very simple markdown parser for bold and newlines
            let formatted = data.answer.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
            formatted = formatted.replace(/\n/g, '<br>');
            answerText.innerHTML = formatted;
            answerText.className = 'answer-text';
        } else {
            answerText.textContent = data.error || 'An error occurred.';
            answerText.className = 'placeholder-text';
        }
    } catch (err) {
        answerText.textContent = 'Failed to connect to the server. Make sure the backend is running.';
        answerText.className = 'placeholder-text';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit';
    }
});
