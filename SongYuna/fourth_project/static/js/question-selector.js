document.addEventListener('DOMContentLoaded', function () {

    /**
     * DOM 요소 가져오기
     * - 각 드롭다운 메뉴
     * - 이미지(Carousel을 보여줄) 영역 
     * - Carousel(슬라이드 이미지) 을 감싸는 요소
     * - views-JSON 'schools_data_json' => JavaScript 'schools-data'
     */
    const schoolSelect = document.getElementById('schoolSelect');
    const yearSelect = document.getElementById('yearSelect');
    const questionSelect = document.getElementById('questionSelect');
    const imageContainer = document.getElementById('image-container');
    const carouselInner = document.querySelector('#imageCarousel .carousel-inner');
    
    const schoolsData = JSON.parse(document.getElementById('schools-data').textContent);


    // 학교 목록 옵션 채우기
    for (const school in schoolsData) {
        const option = document.createElement('option');
        option.value = school;
        option.textContent = school;
        schoolSelect.appendChild(option);
    }


    /* 🔸학교 >> 연도 >> 문항 선택 기능 */

    // 학교 선택 시 -> 연도 목록 동적 생성
    schoolSelect.addEventListener('change',
        function () {
            resetSelect(yearSelect, '연도를 선택하세요');
            resetSelect(questionSelect, '문항을 선택하세요');
            
            // 선택한 학교 저장 - 선택한 학교 연도별 데이터 저장
            const selectedSchool = this.value;
            const years = schoolsData[selectedSchool];
            
            // 학교 선택 and 연도별 저장 시
            // 1) 연도 드롭다운 활성화
            // 2) 연도 옵션 추가
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

    // 연도 선택 시 -> 문항 목록 동적 생성
    yearSelect.addEventListener('change',
        function () {
            // resetSelect 함수 호출!
            resetSelect(questionSelect, '문항을 선택하세요');
            
            // 선택한 학교, 연도 저장 - 선택한 연도 문항 데이터 저장
            const selectedSchool = schoolSelect.value;
            const selectedYear = this.value;
            const questions = schoolsData[selectedSchool]?.[selectedYear];

            // 연도 선택 and 문항별 저장 시
            // 1) 문항 드롭다운 활성화
            // 2) pages 배열(이미지 경로 배열)을 JSON.stringify()로 넣음 ✅
            // 3) 문항 옵션 추가
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

    /* function resetSelect */
    function resetSelect(selectElement, defaultText) {
        if (!selectElement) return;
        
        selectElement.innerHTML = `<option selected disabled>${defaultText}</option>`;
        selectElement.disabled = true;
        
        if (selectElement.id === 'questionSelect' && imageContainer) {
            imageContainer.style.display = 'none';
        }
    }

    /* 🔸이미지 출력 및 타이머 리셋 기능 */

    // 문항 선택 시 -> 이미지 출력 + 타이머 리셋
    questionSelect.addEventListener('change',
        function () {
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
                        // 첫 번째 이미지 'active' 클래스 추가
                        carouselItem.className = i === 0 ? 'carousel-item active' : 'carousel-item';
                        
                        const img = document.createElement('img');
                        img.src = `/static/images/${path}`;
                        img.className = 'd-block w-100';
                        
                        carouselItem.appendChild(img);
                        carouselInner.appendChild(carouselItem);
                    });
                    
                    // 이미지 영역 보여주기 + 타이머 리셋
                    if (imageContainer) imageContainer.style.display = 'block';
                    resetTimer();
                }
            } catch (e) {
                console.error("JSON 파싱 오류:", e);
                if (imageContainer) imageContainer.style.display = 'none';
            }
    });



    /* Timer */
    const timerDisplay = document.getElementById('timerDisplay');
    const minuteInput = document.getElementById('minuteInput');
    const startBtn = document.getElementById('startBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const resetBtn = document.getElementById('resetBtn');
    let timer, seconds = 0, isRunning = false;
    
    // MM:SS
    function updateDisplay() {
        const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
        const secs = String(seconds % 60).padStart(2, '0');
        timerDisplay.textContent = `${mins}:${secs}`;}

    // start
    function startTimer() {
        if (isRunning) return;
        if (seconds === 0) {
            const inputMin = parseInt(minuteInput.value);
            if (isNaN(inputMin) || inputMin <= 0) {
                alert('시간을 입력해주세요.');
                return;
            }
            seconds = inputMin * 60;
            minuteInput.style.display = 'none';
        }

        isRunning = true;
        timer = setInterval(() => {
            if (seconds <= 0) {
                clearInterval(timer);
                isRunning = false;
                alert('시간이 종료되었습니다.')
            } else {
                seconds--;
                updateDisplay();
            }
        }, 1000);
    }

    // stop
    function pauseTimer() {clearInterval(timer); isRunning = false;}
    // reset
    function resetTimer() {clearInterval(timer); isRunning = false; seconds = 0; updateDisplay(); minuteInput.value=''; minuteInput.style.display = 'block'}

    // 버튼 이벤트 연결
    if(startBtn) startBtn.addEventListener('click', startTimer);
    if(pauseBtn) pauseBtn.addEventListener('click', pauseTimer);
    if(resetBtn) resetBtn.addEventListener('click', resetTimer);
});