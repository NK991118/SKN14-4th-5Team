// c:/Workspaces/Personal_Anything/3rd_to_4th/fourth_project/static/js/question-selector.js

document.addEventListener('DOMContentLoaded', function () {

    // --- 1. HTML 요소 찾아오기 (위 HTML의 id와 정확히 일치!) ---
    const schoolSelect = document.getElementById('schoolSelect');
    const yearSelect = document.getElementById('yearSelect');
    const questionSelect = document.getElementById('questionSelect');
    const imageContainer = document.getElementById('image-container');
    const carouselInner = document.querySelector('#imageCarousel .carousel-inner');
    
    const schoolsData = JSON.parse(document.getElementById('schools-data').textContent);

    // --- 2. 학교 목록 채우기 ---
    for (const school in schoolsData) {
        const option = document.createElement('option');
        option.value = school;
        option.textContent = school;
        schoolSelect.appendChild(option);
    }

    // --- 3. 이벤트에 따른 연쇄 반응 설정 ---

    // [반응 1] 학교 선택 시
    schoolSelect.addEventListener('change', function () {
        resetSelect(yearSelect, '연도를 선택하세요');
        resetSelect(questionSelect, '문항을 선택하세요');
        
        const selectedSchool = this.value;
        const years = schoolsData[selectedSchool];

        if (selectedSchool && years) {
            yearSelect.disabled = false;
            for (const year in years) {
                const option = document.createElement('option');
                option.value = year;
                option.textContent = year;
                yearSelect.appendChild(option);
            }
        }
    });

    // [반응 2] 연도 선택 시
    yearSelect.addEventListener('change', function () {
        resetSelect(questionSelect, '문항을 선택하세요');
        
        const selectedSchool = schoolSelect.value;
        const selectedYear = this.value;
        const questions = schoolsData[selectedSchool]?.[selectedYear];

        if (selectedYear && questions) {
            questionSelect.disabled = false;
            for (const num in questions) {
                const option = document.createElement('option');
                option.value = JSON.stringify(questions[num].pages);
                option.textContent = num;
                questionSelect.appendChild(option);
            }
        }
    });

    // [반응 3] 문항 선택 시 (이미지 보여주기)
    questionSelect.addEventListener('change', function () {
        // carouselInner가 없으면 아무것도 안 함 (안전장치)
        if (!carouselInner) {
            console.error("Carousel의 .carousel-inner 요소를 찾을 수 없습니다.");
            return;
        }

        try {
            const pageImagePaths = JSON.parse(this.value);
            carouselInner.innerHTML = ''; // 이전 이미지들 삭제
            
            if (pageImagePaths && pageImagePaths.length > 0) {
                pageImagePaths.forEach((path, i) => {
                    const carouselItem = document.createElement('div');
                    // 첫 번째 아이템에만 'active' 클래스 추가
                    carouselItem.className = i === 0 ? 'carousel-item active' : 'carousel-item';
                    
                    const img = document.createElement('img');
                    img.src = `/static/images/${path}`;
                    img.className = 'd-block w-100';
                    
                    carouselItem.appendChild(img);
                    carouselInner.appendChild(carouselItem);
                });
                
                if (imageContainer) imageContainer.style.display = 'block';
                resetTimer();
            }
        } catch (e) {
            console.error("JSON 파싱 오류:", e);
            if (imageContainer) imageContainer.style.display = 'none';
        }
    });

    // --- 4. 보조 함수 ---

    // 드롭다운 초기화 함수
    function resetSelect(selectElement, defaultText) {
        if (!selectElement) return;
        // HTML의 초기 상태와 똑같이 만들어줌
        selectElement.innerHTML = `<option selected disabled>${defaultText}</option>`;
        selectElement.disabled = true;
        
        if (selectElement.id === 'questionSelect' && imageContainer) {
            imageContainer.style.display = 'none';
        }
    }

    // --- 4. 타이머 로직 (변경 없음) ---
    const timerDisplay = document.getElementById('timerDisplay');
    const startBtn = document.getElementById('startBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const resetBtn = document.getElementById('resetBtn');
    let timer, seconds = 0, isRunning = false;

    function updateDisplay() { /* ... */ }
    function startTimer() { /* ... */ }
    function pauseTimer() { /* ... */ }
    function resetTimer() { /* ... */ }
    
    // 타이머 함수들은 내용이 길어서 생략할게. 이전 코드와 완전히 동일해!
    function updateDisplay() {const hrs = String(Math.floor(seconds / 3600)).padStart(2, '0'); const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0'); const secs = String(seconds % 60).padStart(2, '0'); timerDisplay.textContent = `${hrs}:${mins}:${secs}`;}
    function startTimer() {if (isRunning) return; isRunning = true; timer = setInterval(() => { seconds++; updateDisplay(); }, 1000);}
    function pauseTimer() {clearInterval(timer); isRunning = false;}
    function resetTimer() {clearInterval(timer); isRunning = false; seconds = 0; updateDisplay();}

    // ★★★ 안전장치: 타이머 버튼들이 존재할 때만 이벤트 리스너를 연결! ★★★
    if(startBtn) startBtn.addEventListener('click', startTimer);
    if(pauseBtn) pauseBtn.addEventListener('click', pauseTimer);
    if(resetBtn) resetBtn.addEventListener('click', resetTimer);
});