// c:/Workspaces/Personal_Anything/3rd_to_4th/fourth_project/static/js/my-answer.js (새 파일)

document.addEventListener('DOMContentLoaded', function () {

    // HTML에서 필요한 요소들을 미리 찾아와 변수에 저장
    const schoolSelect = document.getElementById('schoolSelect');
    const yearSelect = document.getElementById('yearSelect');
    const questionSelect = document.getElementById('questionSelect');
    // ★★★ 폼으로 제출할 숨겨진 input 태그를 찾아와! ★★★
    const questionIdInput = document.getElementById('questionIdInput');

    // Django 템플릿에서 받은 대학 데이터를 자바스크립트 객체로 변환
    const schoolsData = JSON.parse(document.getElementById('schools-data').textContent);

    // 학교 선택 메뉴 채우기 (question-selector.js와 동일)
    Object.keys(schoolsData).forEach(school => {
        const option = document.createElement('option');
        option.value = school;
        option.textContent = school;
        schoolSelect.appendChild(option);
    });

    // 학교 선택 시 연도 메뉴 업데이트 (question-selector.js와 동일)
    schoolSelect.addEventListener('change', function () {
        resetSelect(yearSelect, '연도를 선택하세요');
        resetSelect(questionSelect, '문항을 선택하세요');
        questionIdInput.value = ''; // 선택이 바뀌면 숨겨진 값도 초기화
        const selectedSchool = this.value;
        if (selectedSchool) {
            yearSelect.disabled = false;
            const years = schoolsData[selectedSchool];
            Object.keys(years).forEach(year => {
                const option = document.createElement('option');
                option.value = year;
                option.textContent = year;
                yearSelect.appendChild(option);
            });
        }
    });

    // 연도 선택 시 문항 메뉴 업데이트 (question-selector.js와 동일)
    yearSelect.addEventListener('change', function () {
        resetSelect(questionSelect, '문항을 선택하세요');
        questionIdInput.value = '';
        const selectedSchool = schoolSelect.value;
        const selectedYear = this.value;
        if (selectedYear) {
            questionSelect.disabled = false;
            const questions = schoolsData[selectedSchool][selectedYear];
            Object.keys(questions).forEach(num => {
                const option = document.createElement('option');
                // ★★★ 핵심 포인트! ★★★
                // option의 value에 'question_id'를 직접 저장해.
                option.value = questions[num].id; 
                option.textContent = num; // 화면에는 '문항1' 처럼 보이게.
                questionSelect.appendChild(option);
            });
        }
    });
    
    // ★★★ 문항 선택 시, 숨겨진 input의 값을 변경! (이 부분이 제일 달라!) ★★★
    questionSelect.addEventListener('change', function () {
        // 선택된 option의 value (question_id)를 가져와서
        const selectedQuestionId = this.value;
        if (selectedQuestionId) {
            // 숨겨진 input 태그의 value를 선택된 ID로 설정해줘.
            // 이제 폼을 제출하면 이 값이 'question_id'라는 이름으로 서버에 전송될 거야.
            questionIdInput.value = selectedQuestionId;
            console.log(`선택된 문제 ID가 '${selectedQuestionId}'(으)로 설정되었습니다.`);
        } else {
            questionIdInput.value = '';
        }
    });

    // 드롭다운 메뉴 초기화 함수 (question-selector.js와 동일)
    function resetSelect(selectElement, defaultText) {
        selectElement.innerHTML = '';
        const defaultOption = document.createElement('option');
        defaultOption.textContent = defaultText;
        defaultOption.selected = true;
        defaultOption.disabled = true;
        selectElement.appendChild(defaultOption);
        selectElement.disabled = true;
    }

    // --- 이미지 업로드 미리보기 로직 ---
    const imageUploader = document.getElementById('imageUploader');
    const imagePreview = document.getElementById('imagePreview');
    const previewText = document.getElementById('previewText');
    
    // 파일 업로드 input에 변화가 생기면 실행
    imageUploader.addEventListener('change', function(event) {
        const file = event.target.files[0]; // 사용자가 선택한 파일
        if (file) {
            const reader = new FileReader(); // 파일을 읽기 위한 객체
            reader.onload = function(e) {
                // 파일 읽기가 완료되면, img 태그의 src를 읽어온 파일 데이터로 설정
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block'; // 숨겨져 있던 img 태그를 보여줘.
                previewText.style.display = 'none'; // "미리보기 표시" 텍스트는 숨겨.
            }
            reader.readAsDataURL(file); // 파일을 Data URL 형태로 읽기 시작
        }
    });
});