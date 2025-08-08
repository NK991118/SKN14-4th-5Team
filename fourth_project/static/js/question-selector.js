document.addEventListener('DOMContentLoaded', function () {

    const schoolSelect = document.getElementById('schoolSelect');
    const yearSelect = document.getElementById('yearSelect');
    const questionSelect = document.getElementById('questionSelect');
    const imageContainer = document.getElementById('image-container');
    const carouselInner = document.querySelector('#imageCarousel .carousel-inner');
    
    const schoolsData = JSON.parse(document.getElementById('schools-data').textContent);

    for (const school in schoolsData) {
        const option = document.createElement('option');
        option.value = school;
        option.textContent = school;
        schoolSelect.appendChild(option);
    }

    schoolSelect.addEventListener('change',
        function () {
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

    // 연도 선택 시 -> 문항 목록 동적 생성
    yearSelect.addEventListener('change',
        function () {
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

    function resetSelect(selectElement, defaultText) {
        if (!selectElement) return;
        
        selectElement.innerHTML = `<option selected disabled>${defaultText}</option>`;
        selectElement.disabled = true;
        
        if (selectElement.id === 'questionSelect' && imageContainer) {
            imageContainer.style.display = 'none';
        }
    }

    questionSelect.addEventListener('change',
        function () {

            if (!carouselInner) {
                console.error("Carousel의 .carousel-inner 요소를 찾을 수 없습니다.");
                return;
            }

            try {
                const pageImagePaths = JSON.parse(this.value);
                carouselInner.innerHTML = '';
                
                if (pageImagePaths && pageImagePaths.length > 0) {
                    pageImagePaths.forEach((path, i) => {
                        const carouselItem = document.createElement('div');

                        carouselItem.className = i === 0 ? 'carousel-item active' : 'carousel-item';
                        
                        const img = document.createElement('img');
                        img.src = `/static/images/${path}`;
                        // img.className = 'd-block w-100';
                        img.className = 'd-block';
                        img.style.width = '100%';
                        img.style.height = 'auto';
                        
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



    /* Timer */
    const timerDisplay = document.getElementById('timerDisplay');
    const minuteInput = document.getElementById('minuteInput');
    const startBtn = document.getElementById('startBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const resetBtn = document.getElementById('resetBtn');
    let timer, seconds = 0, isRunning = false;

    function updateDisplay() {
        const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
        const secs = String(seconds % 60).padStart(2, '0');
        timerDisplay.textContent = `${mins}:${secs}`;}

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

    function pauseTimer() {clearInterval(timer); isRunning = false;}

    function resetTimer() {clearInterval(timer); isRunning = false; seconds = 0; updateDisplay(); minuteInput.value=''; minuteInput.style.display = 'block'}

    if(startBtn) startBtn.addEventListener('click', startTimer);
    if(pauseBtn) pauseBtn.addEventListener('click', pauseTimer);
    if(resetBtn) resetBtn.addEventListener('click', resetTimer);
});