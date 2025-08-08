document.addEventListener('DOMContentLoaded', function () {

    const schoolSelect = document.getElementById('schoolSelect');
    const yearSelect = document.getElementById('yearSelect');
    const questionSelect = document.getElementById('questionSelect');

    const questionIdInput = document.getElementById('questionIdInput');

    const schoolsData = JSON.parse(document.getElementById('schools-data').textContent);

    Object.keys(schoolsData).forEach(school => {
        const option = document.createElement('option');
        option.value = school;
        option.textContent = school;
        schoolSelect.appendChild(option);
    });

    schoolSelect.addEventListener('change', function () {
        resetSelect(yearSelect, '연도를 선택하세요');
        resetSelect(questionSelect, '문항을 선택하세요');
        questionIdInput.value = '';
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

                option.value = questions[num].id; 
                option.textContent = num;
                questionSelect.appendChild(option);
            });
        }
    });

    questionSelect.addEventListener('change', function () {

        const selectedQuestionId = this.value;
        if (selectedQuestionId) {

            questionIdInput.value = selectedQuestionId;
            console.log(`선택된 문제 ID가 '${selectedQuestionId}'(으)로 설정되었습니다.`);
        } else {
            questionIdInput.value = '';
        }
    });

    function resetSelect(selectElement, defaultText) {
        selectElement.innerHTML = '';
        const defaultOption = document.createElement('option');
        defaultOption.textContent = defaultText;
        defaultOption.selected = true;
        defaultOption.disabled = true;
        selectElement.appendChild(defaultOption);
        selectElement.disabled = true;
    }

    const imageUploader = document.getElementById('imageUploader');
    const imagePreview = document.getElementById('imagePreview');
    const previewText = document.getElementById('previewText');

    imageUploader.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block'; 
                previewText.style.display = 'none'; 
            }
            reader.readAsDataURL(file);
        }
    });

        const gradingForm = document.getElementById('grading-form');
    const spinner = document.getElementById('spinner');
    console.log(spinner);

    
    gradingForm.addEventListener('submit',
        function (e) {
            e.preventDefault();

            const fileInput = document.getElementById('imageUploader');
            if (!fileInput.files.length) {
                alert('작성한 답안 이미지 파일을 업로드해주세요.')
                return;
            }

            spinner.style.display = 'block';

            gradingForm.submit();
    });
});