document.addEventListener('DOMContentLoaded', function () {
   
    const schoolSelect = document.getElementById('schoolSelect');
    const yearSelect = document.getElementById('yearSelect');
    const questionSelect = document.getElementById('questionSelect');

    const questionIdInput = document.getElementById('questionIdInput');

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
    
    questionSelect.addEventListener('change', function () {
        const selectedQuestionId = this.value; // question_id
        if (selectedQuestionId) {
            questionIdInput.value = selectedQuestionId;
            console.log(`선택된 문제 ID가 '${selectedQuestionId}'(으)로 설정되었습니다.`);
        } else {
            questionIdInput.value = '';
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

    // --- 이미지 업로드 미리보기 ---
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