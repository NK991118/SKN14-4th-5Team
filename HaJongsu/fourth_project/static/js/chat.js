// c:/Workspaces/Personal_Anything/3rd_to_4th/fourth_project/static/js/chat.js (최종 완성본)

// 웹 페이지의 모든 HTML 요소가 로드된 후에 이 스크립트 전체를 실행하라는 약속이야.
// 이렇게 하면 getElementById 같은 함수가 요소를 못 찾는 일을 방지할 수 있어.
document.addEventListener('DOMContentLoaded', function() {
    
    // --- [사전 준비] 채팅 기능에 필요한 모든 HTML 요소를 미리 찾아와서 변수에 담아둬. ---
    // 이렇게 하면 코드를 읽기 쉽고, 나중에 수정하기도 편해.
    const chatForm = document.getElementById('chat-form');       // 메시지 입력 폼 <form>
    const chatInput = document.getElementById('chat-input');     // 메시지 입력 칸 <input>
    const chatHistory = document.getElementById('chat-history'); // 채팅 내용이 표시될 <div>

    // [안전 장치] 만약 이 페이지에 채팅 폼이 없다면 (예: 메인 페이지),
    // 괜히 에러를 일으키지 말고 여기서 스크립트 실행을 조용히 중단해.
    if (!chatForm) {
        return;
    }

    // --- [이벤트 연결] 사용자가 메시지를 전송할 때 어떤 일을 할지 정해줘. ---
    // 'submit' 이벤트는 사용자가 전송 버튼을 누르거나 엔터 키를 쳤을 때 발생해.
    chatForm.addEventListener('submit', function(event) {
        // 1. 폼을 제출하면 페이지가 새로고침되는 기본 동작을 막아. AJAX 통신의 핵심!
        event.preventDefault();

        // 2. 사용자가 입력한 메시지를 가져오고, .trim()으로 양쪽의 불필요한 공백을 제거해.
        const userMessage = chatInput.value.trim();

        // 3. 만약 메시지가 비어있다면, 아무것도 안 하고 조용히 함수를 종료해.
        if (!userMessage) {
            return;
        }

        // 4. 내가 보낸 메시지를 화면에 즉시 추가해. (사용자 경험 향상)
        addMessageToHistory(userMessage, 'user');
        
        // 5. AI에게 질문을 보냈으니, 입력창은 깨끗하게 비워줘.
        chatInput.value = '';
        
        // 6. "AI가 생각 중..."이라는 로딩 애니메이션을 보여줘.
        showLoadingIndicator();
        
        // 7. 백엔드에 실제로 AI의 답변을 요청하는 함수를 호출해.
        getAiResponse(userMessage);
    });

    // --- [핵심 기능 함수들] ---
    // 이 함수들은 모두 document.addEventListener 안에 있어서, 위에서 선언한 변수(chatHistory 등)를 모두 알고 있어.

    /**
     * 채팅창에 새로운 말풍선을 추가하는 함수
     * @param {string} message - 표시할 메시지 내용
     * @param {string} sender - 메시지를 보낸 사람 ('user' 또는 'ai')
     */
    function addMessageToHistory(message, sender) {
        // 1. 새로운 말풍선이 될 <div> 요소를 만들어.
        const messageElement = document.createElement('div');
        
        // 2. CSS 스타일을 적용하기 위해 클래스를 추가해. 
        //    'chat-message'는 모든 말풍선의 공통 스타일, 'user-message'나 'ai-message'는 각각의 스타일이야.
        messageElement.classList.add('chat-message', sender === 'user' ? 'user-message' : 'ai-message');
        
        // 3. 보낸 사람이 AI일 경우, 마크다운 형식의 텍스트를 HTML로 변환해서 보여줘.
        if (sender === 'ai') {
            // marked.parse()는 base.html에 추가한 marked.js 라이브러리가 제공하는 마법의 함수야.
            messageElement.innerHTML = marked.parse(message);
        } else {
            // 사용자가 보낸 메시지는 해킹 위험이 있을 수 있으니, 안전하게 textContent로 넣어줘.
            messageElement.textContent = message;
        }
        
        // 4. 완성된 말풍선을 채팅 기록 영역에 추가해.
        chatHistory.appendChild(messageElement);

        // 5. 새 메시지가 추가되면, 스크롤을 항상 맨 아래로 내려주는 마법의 코드!
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
    /**
     * '입력 중...' 로딩 애니메이션을 채팅창에 추가하는 함수
     */
    function showLoadingIndicator() {
        // 1. 만약 이미 로딩 애니메이션이 있다면, 또 추가하지 않도록 막아줘.
        if (document.getElementById('loading-indicator')) return;

        // 2. 로딩 애니메이션 전체를 감싸는 <div>를 만들어.
        const loadingElement = document.createElement('div');
        loadingElement.id = 'loading-indicator'; // 나중에 쉽게 찾아서 지울 수 있도록 ID를 부여해.
        loadingElement.classList.add('chat-message', 'ai-message'); // AI 말풍선처럼 보이게 스타일을 적용해.
        
        // 3. 점 3개를 담을 컨테이너를 만들어. (CSS 애니메이션을 위해)
        const dotsContainer = document.createElement('div');
        dotsContainer.classList.add('loading-dots');
        
        // 4. 반복문으로 점 3개를 만들어서 컨테이너에 넣어줘.
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            dotsContainer.appendChild(dot);
        }
        
        // 5. 완성된 점들을 로딩 요소에 넣고, 그걸 다시 채팅 기록에 추가해.
        loadingElement.appendChild(dotsContainer);
        chatHistory.appendChild(loadingElement);

        // 6. 로딩 애니메이션이 보이도록 스크롤을 맨 아래로 내려줘.
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    /**
     * 채팅창에서 로딩 애니메이션을 제거하는 함수
     */
    function hideLoadingIndicator() {
        const loadingElement = document.getElementById('loading-indicator');
        // 로딩 요소가 존재할 경우에만, 그걸 찾아서 제거해.
        if (loadingElement) {
            loadingElement.remove();
        }
    }

    /**
     * 백엔드 API에 AI 응답을 요청하는 함수 (AJAX 통신)
     * @param {string} message - 사용자가 입력한 질문
     */
    function getAiResponse(message) {
        // 1. Django의 보안 기능(CSRF)을 통과하기 위한 토큰을 폼에서 가져와.
        const csrfToken = chatForm.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // 2. 현재 보고 있는 첨삭 기록의 고유 ID를 폼의 data-* 속성에서 가져와.
        const submissionId = chatForm.dataset.submissionId;

        // 3. [안전 장치] 만약 ID를 가져오지 못했다면, 백엔드에 요청을 보내지 않고 사용자에게 오류를 알려줘.
        if (!submissionId) {
            hideLoadingIndicator(); // 로딩 애니메이션은 일단 숨겨주고,
            addMessageToHistory("오류: 첨삭 기록 ID를 찾을 수 없습니다. 페이지를 새로고침 해주세요.", "ai");
            return; // 함수를 여기서 종료.
        }

        // 4. fetch 함수를 사용해서 백엔드 '/api/chat/' 주소로 데이터를 보내.
        fetch('/api/chat/', {
            method: 'POST', // 데이터를 보내는 거니까 POST 방식
            headers: {
                'Content-Type': 'application/json', // "우리가 보내는 건 JSON 형식이야" 라고 알려줘.
                'X-CSRFToken': csrfToken, // Django CSRF 보안 토큰을 헤더에 담아 보내.
            },
            // 5. 실제 보낼 데이터. 사용자의 질문과 첨삭 ID를 JSON 문자열로 변환해서 담아줘.
            body: JSON.stringify({ 
                message: message,
                submission_id: submissionId 
            })
        })
        .then(response => {
            hideLoadingIndicator(); // 6. 응답을 받으면(성공이든 실패든) 일단 로딩 애니메이션부터 숨겨.
            if (!response.ok) { // 7. 만약 응답이 성공(200 OK)이 아니라면,
                // 서버가 보낸 에러 메시지를 포함해서 에러를 발생시켜 catch 블록으로 보내.
                return response.json().then(err => { throw new Error(err.error || '서버 응답 오류'); });
            }
            return response.json(); // 8. 성공했다면, 응답 데이터를 JSON 객체로 변환해.
        })
        .then(data => {
            // 9. JSON 객체 안에 'ai_message'가 있다면, 그걸 화면에 추가해.
            if (data.ai_message) {
                addMessageToHistory(data.ai_message, 'ai');
            }
        })
        .catch(error => {
            // 10. fetch 과정에서 어떤 에러라도 발생하면 여기서 잡아서 사용자에게 보여줘.
            hideLoadingIndicator(); // 에러가 나도 로딩 애니메이션은 꼭 숨겨야 해.
            console.error('Error:', error); // 개발자를 위해 콘솔에 자세한 에러를 남겨.
            addMessageToHistory(`죄송합니다, AI와 통신 중 오류가 발생했습니다: ${error.message}`, 'ai');
        });
    }   

}); // document.addEventListener의 닫는 괄호. 모든 코드는 이 안에 있어야 해.