// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Elements
document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.querySelector('textarea[data-api-input]');
    const magicButton = document.querySelector('.fa-wand-magic-sparkles').parentElement;
    const actionButtons = document.querySelectorAll('.action-button');
    const loadingOverlay = document.getElementById('loading-overlay');

    // Toast notification function
    function showToast(message, type = 'error') {
        const toastContainer = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type} flex items-center p-4 mb-4 rounded-lg shadow-lg`;
        toast.innerHTML = `
            <i class="fas ${type === 'error' ? 'fa-exclamation-circle text-red-500' : 'fa-check-circle text-green-500'} mr-2"></i>
            <span>${message}</span>
        `;
        toastContainer.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Loading state handler
    function setLoading(isLoading) {
        if (isLoading) {
            loadingOverlay.classList.remove('hidden');
            loadingOverlay.classList.add('flex');
            magicButton.classList.add('animate-pulse');
            textarea.disabled = true;
        } else {
            loadingOverlay.classList.add('hidden');
            loadingOverlay.classList.remove('flex');
            magicButton.classList.remove('animate-pulse');
            textarea.disabled = false;
        }
    }

    // Generate response using Deep Seek API
    async function generateResponse(prompt) {
        try {
            setLoading(true);
            const response = await fetch(`${API_BASE_URL}/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `API request failed with status ${response.status}`);
            }

            const data = await response.json();
            if (data.error) {
                throw new Error(data.error);
            }

            // Extract content from Deep Seek API response
            const content = data.choices?.[0]?.message?.content;
            if (!content) {
                throw new Error('Invalid response format from API');
            }

            showToast('Response generated successfully!', 'success');
            return content;
        } catch (error) {
            console.error('Error:', error);
            showToast(error.message || 'Failed to generate response');
            return null;
        } finally {
            setLoading(false);
        }
    }

    // Event Listeners
    if (magicButton) {
        magicButton.addEventListener('click', async () => {
            const prompt = textarea.value.trim();
            if (!prompt) {
                showToast('Please enter a prompt first');
                return;
            }

            const response = await generateResponse(prompt);
            if (response) {
                textarea.value = response;
                textarea.style.height = 'auto';
                textarea.style.height = (textarea.scrollHeight) + 'px';
            }
        });
    }

    // Handle action button clicks
    actionButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const action = button.querySelector('span').textContent;
            textarea.value = `Help me ${action.toLowerCase()}`;
            textarea.style.height = 'auto';
            textarea.style.height = (textarea.scrollHeight) + 'px';
            
            // Add animation to the magic button
            magicButton.querySelector('i').classList.add('animating');
            setTimeout(() => {
                magicButton.querySelector('i').classList.remove('animating');
            }, 1000);
        });
    });

    // Auto-resize textarea
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }

    // Health check on load
    fetch(`${API_BASE_URL}/health`)
        .then(response => response.json())
        .then(data => {
            console.log('API Status:', data.status);
            if (!data.api_key_configured) {
                showToast('API key not configured. Some features may be limited.');
            }
        })
        .catch(error => {
            console.error('API Health Check Failed:', error);
            showToast('Failed to connect to the API server');
        });
});