물론이지! 깃허브 저장소의 얼굴인 README.md는 정말 중요해. 우리가 지금까지 함께 만든 기능과 구조를 다른 사람들이나 미래의 네가 봤을 때 한눈에 알아볼 수 있도록, 아주 깔끔하고 전문적인 README.md 파일을 만들어 줄게.

이 파일은 프로젝트의 가장 최상위 폴더 (즉, manage.py와 .gitignore가 있는 곳)에 README.md 라는 이름으로 저장하면 돼.

README.md (추천 내용)
Generated markdown
# 🤖 AI 논술 첨삭 멘토봇 (Django 버전)

**대학 논술 전형 대비를 위한 Django 기반 AI 논술 첨삭 웹 애플리케이션**

이 프로젝트는 기존 Streamlit으로 구현되었던 프로토타입을, 보다 확장성 있고 안정적인 웹 프레임워크인 Django와 Bootstrap을 사용하여 웹 애플리케이션으로 재구축한 것입니다. 사용자가 직접 작성한 논술 답안 이미지를 업로드하면, AI가 대학별 채점 기준과 모범 답안을 바탕으로 구조적인 피드백을 제공합니다.

---

## ✨ 주요 기능

*   **🔐 사용자 인증:** Django 기본 인증 시스템을 활용한 회원가입, 로그인, 로그아웃 기능.
*   **📚 문제 선택 및 열람:**
    *   대학, 연도, 문항별로 정리된 기출문제를 동적으로 선택 가능.
    *   PDF를 고화질 이미지로 변환하여, 한 페이지씩 넘겨볼 수 있는 깔끔한 캐러셀 뷰어 제공.
*   **✍️ 답안 제출:**
    *   사용자가 직접 쓴 답안지 이미지 파일 업로드 기능.
    *   PaddleOCR을 이용해 업로드된 이미지에서 텍스트를 정확하게 추출.
*   **🤖 AI 첨삭:**
    *   LangChain과 RAG(검색 증강 생성) 기술을 활용.
    *   FAISS 벡터 DB에 저장된 대학별 채점 기준과 모범 답안을 바탕으로 맥락에 맞는 첨삭 제공.
*   **📈 첨삭 히스토리:**
    *   모든 첨삭 결과를 사용자와 연결하여 데이터베이스에 영구 저장.
    *   '나의 첨삭 히스토리' 페이지에서 자신의 지난 기록들을 최신순으로 확인하고, 상세 내용을 다시 볼 수 있는 기능.

---

## 🛠️ 기술 스택

| 구분 | 기술 |
| :--- | :--- |
| **Backend** | Python, Django |
| **Frontend** | HTML, CSS, JavaScript, Bootstrap 5 |
| **AI / LLM** | LangChain, OpenAI API (`gpt-4o-mini`) |
| **Vector DB** | FAISS (Facebook AI Similarity Search) |
| **OCR** | PaddleOCR |
| **Etc** | PyMuPDF (PDF 처리) |

---

## 🚀 실행 방법 (Getting Started)

#### 1. 저장소 복제 (Clone)

```bash
git clone https://github.com/dreamwars99/Personal_Anything.git
cd Personal_Anything

2. 가상 환경 설정 및 활성화
Generated bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
3. 필요 라이브러리 설치
Generated bash
pip install -r requirements.txt```

#### 4. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고, OpenAI API 키를 입력하세요.
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

OPENAI_API_KEY="sk-..."

Generated code
#### 5. 데이터베이스 설정

```bash
python manage.py migrate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
6. 데이터 전처리 (최초 1회 실행)

중요: 실행 전, static/pdf/ 와 data/json/ 폴더에 각 대학별 논술 자료를 올바른 위치에 넣어주세요.

Generated bash
# 1. PDF 파일을 이미지로 변환합니다.
python convert_pdfs.py

# 2. JSON과 이미지 데이터를 기반으로 config.py 파일을 자동 생성합니다.
python generate_config.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
7. 관리자 계정 생성

로그인 테스트 및 관리자 페이지 접근을 위해 관리자 계정을 생성합니다.

Generated bash
python manage.py createsuperuser
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
8. 개발 서버 실행
Generated bash
python manage.py runserver
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

이제 웹 브라우저에서 http://127.0.0.1:8000 주소로 접속하여 애플리케이션을 확인할 수 있습니다.

🌱 향후 계획 (Future Work)

📝 나만의 오답노트: 사용자가 중요한 첨삭 결과를 따로 저장하고 모아볼 수 있는 기능.

📊 성장 대시보드: AI가 매긴 예상 점수를 그래프로 시각화하여 학습 성과를 추적하는 기능.

🔗 유사 문제 추천: 약점을 보완할 수 있는 유사한 유형의 다른 대학 문제를 추천하는 AI 기능.