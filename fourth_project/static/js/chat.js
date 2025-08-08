document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');      
    const chatInput = document.getElementById('chat-input');     
    const chatHistory = document.getElementById('chat-history'); 
    if (!chatForm) {
        return;
    }
    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const userMessage = chatInput.value.trim();
        if (!userMessage) {
            return;
        }
        addMessageToHistory(userMessage, 'user');
        chatInput.value = '';
        showLoadingIndicator();
        getAiResponse(userMessage);
    });
    function addMessageToHistory(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', sender === 'user' ? 'user-message' : 'ai-message');
        if (sender === 'ai') {
            messageElement.innerHTML = marked.parse(message);
        } else {
            messageElement.textContent = message;
        }
        chatHistory.appendChild(messageElement);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    function showLoadingIndicator() {
        if (document.getElementById('loading-indicator')) return;
        const loadingElement = document.createElement('div');
        loadingElement.id = 'loading-indicator';
        loadingElement.classList.add('chat-message', 'ai-message'); 
        const dotsContainer = document.createElement('div');
        dotsContainer.classList.add('loading-dots');
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            dotsContainer.appendChild(dot);
        }
        loadingElement.appendChild(dotsContainer);
        chatHistory.appendChild(loadingElement);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    function hideLoadingIndicator() {
        const loadingElement = document.getElementById('loading-indicator');
        if (loadingElement) {
            loadingElement.remove();
        }
    }

    /**
     * 백엔드 API에 AI 응답을 요청하는 함수 (AJAX 통신)
     * @param {string} message - 사용자가 입력한 질문
     */
    function getAiResponse(message) {
        const csrfToken = chatForm.querySelector('[name=csrfmiddlewaretoken]').value;
        const submissionId = chatForm.dataset.submissionId;
        if (!submissionId) {
            hideLoadingIndicator(); 
            addMessageToHistory("오류: 첨삭 기록 ID를 찾을 수 없습니다. 페이지를 새로고침 해주세요.", "ai");
            return; 
        }
        fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', 
                'X-CSRFToken': csrfToken, 
            },
            body: JSON.stringify({ 
                message: message,
                submission_id: submissionId 
            })
        })
        .then(response => {
            hideLoadingIndicator(); 
            if (!response.ok) { 
                return response.json().then(err => { throw new Error(err.error || '서버 응답 오류'); });
            }
            return response.json(); 
        })
        .then(data => {
            if (data.ai_message) {
                addMessageToHistory(data.ai_message, 'ai');
            }
        })
        .catch(error => {
            hideLoadingIndicator();
            console.error('Error:', error);
            addMessageToHistory(`죄송합니다, AI와 통신 중 오류가 발생했습니다: ${error.message}`, 'ai');
        });
    }   

}); 