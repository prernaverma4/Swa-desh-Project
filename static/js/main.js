/**
 * Digital Catalyst - Main JavaScript
 * Handles animations, interactions, and dynamic features
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Animate stat cards on load
    animateStatCards();
    
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Auto-hide flash messages after 5 seconds
    autoHideFlashMessages();
    
    // Add form validation feedback
    enhanceFormValidation();
    
    // Chatbot widget
    initChatbot();
});

/**
 * Chatbot widget - toggle, send message, display response
 */
function initChatbot() {
    const toggle = document.getElementById('chatbot-toggle');
    const panel = document.getElementById('chatbot-panel');
    const closeBtn = document.getElementById('chatbot-close');
    const input = document.getElementById('chatbot-input');
    const sendBtn = document.getElementById('chatbot-send');
    const messagesEl = document.getElementById('chatbot-messages');

    if (!toggle || !panel || !messagesEl) return;

    function openPanel() {
        panel.hidden = false;
        input.focus();
    }
    function closePanel() {
        panel.hidden = true;
    }
    function scrollToBottom() {
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    toggle.addEventListener('click', function() {
        if (panel.hidden) openPanel();
        else closePanel();
    });
    closeBtn.addEventListener('click', closePanel);

    function addMessage(text, isBot) {
        const wrap = document.createElement('div');
        wrap.className = 'chatbot-msg ' + (isBot ? 'bot' : 'user');
        const bubble = document.createElement('div');
        bubble.className = 'chatbot-bubble';
        if (isBot) {
            bubble.innerHTML = text;
        } else {
            bubble.textContent = text;
        }
        wrap.appendChild(bubble);
        messagesEl.appendChild(wrap);
        scrollToBottom();
    }

    function setLoading(loading) {
        sendBtn.disabled = loading;
        const icon = sendBtn.querySelector('i');
        if (icon) icon.className = loading ? 'bi bi-hourglass-split' : 'bi bi-send-fill';
    }

    function sendMessage() {
        const text = (input.value || '').trim();
        if (!text) return;
        input.value = '';
        addMessage(text, false);
        setLoading(true);

        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
            .then(function(res) { return res.json(); })
            .then(function(data) {
                setLoading(false);
                addMessage(data.response || 'Sorry, I could not process that.', true);
            })
            .catch(function() {
                setLoading(false);
                addMessage('Something went wrong. Please try again.', true);
            });
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
}

/**
 * Animate stat cards with staggered entrance
 */
function animateStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

/**
 * Add smooth scrolling to anchor links
 */
function addSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Auto-hide flash messages after 5 seconds
 */
function autoHideFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = bootstrap.Alert.getOrCreateInstance ? bootstrap.Alert.getOrCreateInstance(message) : new bootstrap.Alert(message);
                if (bsAlert && bsAlert.close) bsAlert.close();
            } else {
                message.style.display = 'none';
            }
        }, 5000);
    });
}

/**
 * Enhance form validation with custom styling
 */
function enhanceFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Format numbers with Indian numbering system
 */
function formatIndianNumber(num) {
    const x = num.toString();
    const lastThree = x.substring(x.length - 3);
    const otherNumbers = x.substring(0, x.length - 3);
    
    if (otherNumbers !== '') {
        return otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + "," + lastThree;
    }
    
    return lastThree;
}

/**
 * Debounce function for search inputs
 */
function debounce(func, wait) {
    let timeout;
    
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Add loading state to buttons
 */
function addLoadingState(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Loading...';
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText;
    }
}
