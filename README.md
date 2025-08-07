

# 🤖 AI 논술 첨삭 멘토봇 (Django 버전)

**대학 논술 전형 대비를 위한 Django 기반 AI 논술 첨삭 웹 애플리케이션**

이 프로젝트는 기존 Streamlit으로 구현되었던 프로토타입을, 보다 확장성 있고 안정적인 웹 프레임워크인 Django와 Bootstrap을 사용하고, AWS로 실제 배포 가능한 웹 애플리케이션으로 재구축한 것입니다. 사용자가 직접 작성한 논술 답안 이미지를 업로드하면, AI가 대학별 채점 기준과 모범 답안을 바탕으로 구조적인 피드백을 제공합니다.


## ⏰프로젝트 기간
2025-08-07 ~ 2025-08-08


# 🧭기존 프로젝트 소개 (streamlit 버전)

## 👨‍💻 팀원 소개 및 역할
#### 팀명: 오논아놈? (오 논술할 줄 아는 놈인가?)
| **하종수** |             **김성민**              | **송유나** | **이나경** | **이승혁** |
|:--:|:--------------------------------:|:--:|:--:|:--:|
| ![](image/짱구.png) |![](image/맹구.png) | ![](image/액션가면.png) | ![](image/부리부리대마왕.jpeg) | |)
 |
| 프로젝트 총괄, 데이터 수집·전처리 | 프론트엔드 개발 (Streamlit), 데이터 수집·전처리 | 데이터 전처리, 백엔드 개발 (RAG) | 데이터 전처리, 백엔드 개발 (RAG) | 백엔드 개발 (RAG), 프롬프팅 |

---

## 🎯 프로젝트 주제
**개인 맞춤형 AI 논술 과외 튜터 개발**

---

## 🔥프로젝트 소개
### 서비스명: 논스루(through)
LLM 기반의 RAG(Retrieval-Augmented Generation) 구조를 활용한 **대학 논술 첨삭 보조 시스템**입니다.
사용자가 작성한 논술 답안을 OCR 처리하고 이를 바탕으로 관련 문항의 채점 기준과 예시답안을 검색하고 분석하여, AI가 **구체적이고 구조적인 피드백**을 제공해줍니다. 또한, 사용자가 입력한 자신의 답안을 기반으로 **Q&A 챗봇** 기능도 지원하여, 자주 묻는 질문이나 구체적인 문장 단위의 피드백 요청도 가능합니다.


---

# 💡 이하 Django version 추가 사항


## ✨ 주요 기능 및 추가 사항

*   **🔐 사용자 인증:**
    * Django 기본 인증 시스템을 활용한 회원가입, 로그인, 로그아웃

*   **⏏️ 주요 추가사항:**
    * 첨삭 히스토리, 향상된 챗봇 및 UI/UX 개선

*   **📚 문제 선택 및 열람:**
    *   대학, 연도, 문항별로 정리된 기출문제를 동적으로 선택 가능.
    *   PDF를 고화질 이미지로 변환하여, 한 페이지씩 넘겨볼 수 있는 깔끔한 캐러셀 뷰어 제공.
*   **✍️ 답안 제출:**
    *   사용자가 직접 쓴 답안지 이미지 파일 업로드 기능.
    *   PaddleOCR을 이용해 업로드된 이미지에서 텍스트를 정확하게 추출.
*   **🤖 AI 첨삭:**
    *   LangChain과 RAG(검색 증강 생성) 기술을 활용.
    *   FAISS 벡터 DB에 저장된 대학별 채점 기준과 모범 답안을 바탕으로 맥락에 맞는 첨삭 제공.

*   **💖 UI/UX 개선:**
    * streamlit의 한계를 극복하여 django와 bootstrap을 이용한 UI/UX 개선

*   **📜 자료 업데이트를 염두에 둔 자동화 코드 추가:**
    * 추가된 대학 자료 업데이트를 염두에 둔 pdf -> png 변환 / 대학 데이터 업데이트 코드 추가

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
| **Deploy** | AWS |

---


## ⚙️ 웹앱 구성도 및 플로우차트


### 시스템 아키텍처
<img width="4905" height="3226" alt="skn14_4th_5team_system_architecture" src="https://github.com/user-attachments/assets/d5593a93-0014-481c-ab49-e6fc81413e23" />



### 데이터 플로우
<img width="1828" height="830" alt="skn14_4th_5team_data_flow" src="https://github.com/user-attachments/assets/aca8a742-d045-4cc5-b6c0-be4c3337e696" />



### 유저 플로우

<img width="1022" height="842" alt="skn14_4th_5team_user_flow" src="https://github.com/user-attachments/assets/3bdc5350-d960-48c8-a819-35aa7c6a11ee" />



## 🚀 실행 방법 (Getting Started)

#### 1. 저장소 복제 (Clone)

```bash
git clone https://github.com/skn-ai14-250409/SKN14-4th-5Team.git
```
#### 2. 가상 환경 설정 및 활성화

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. 필요 라이브러리 설치
```bash
pip install -r requirements.txt
```

#### 4. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고, OpenAI API 키를 입력하세요.
```bash
OPENAI_API_KEY="sk-..."
```

#### 5. 데이터베이스 설정


#### 6. 데이터 전처리 (최초 1회 실행)

중요: 실행 전, static/pdf/ 와 data/json/ 폴더에 각 대학별 논술 자료를 올바른 위치에 넣어주세요.


1. PDF 파일을 이미지로 변환합니다.
```bash
python convert_pdfs.py
```

2. JSON과 이미지 데이터를 기반으로 config.py 파일을 자동 생성합니다.
```bash
python generate_config.py
```
#### 7. 관리자 계정 생성

로그인 테스트 및 관리자 페이지 접근을 위해 관리자 계정을 생성합니다.


#### 8. 개발 서버 실행

```bash
python manage.py runserver
```

이제 웹 브라우저에서 http://127.0.0.1:8000 주소로 접속하여 애플리케이션을 확인할 수 있습니다.

#### 🌱 향후 계획 (Future Work)

📝 나만의 오답노트: 사용자가 중요한 첨삭 결과를 따로 저장하고 모아볼 수 있는 기능.

📊 성장 대시보드: AI가 매긴 예상 점수를 그래프로 시각화하여 학습 성과를 추적하는 기능.

🔗 유사 문제 추천: 약점을 보완할 수 있는 유사한 유형의 다른 대학 문제를 추천하는 AI 기능.
