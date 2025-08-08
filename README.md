

# 🤖 AI 논술 첨삭 멘토봇 (Django 버전)

**대학 논술 전형 대비를 위한 Django 기반 AI 논술 첨삭 웹 애플리케이션**

이 프로젝트는 기존 Streamlit으로 구현되었던 프로토타입을, 보다 확장성 있고 안정적인 웹 프레임워크인 Django와 Bootstrap을 사용하고, AWS로 실제 배포 가능한 웹 애플리케이션으로 재구축한 것입니다. 사용자가 직접 작성한 논술 답안 이미지를 업로드하면, AI가 대학별 채점 기준과 모범 답안을 바탕으로 구조적인 피드백을 제공합니다.


## ⏰프로젝트 기간
2025-08-07 ~ 2025-08-08

## 👨‍💻 팀원 소개 및 역할
#### 팀명: 오논아놈? (오 논술할 줄 아는 놈인가?)
| **하종수** |             **김성민**              | **송유나** | **이나경** | **이승혁** |
|:--:|:--------------------------------:|:--:|:--:|:--:|
| <img width="292" height="337" alt="짱구" src="https://github.com/user-attachments/assets/08447ca7-e05d-4c34-9be8-7a8145c15523" /> | <img width="340" height="420" alt="맹구" src="https://github.com/user-attachments/assets/aee11e37-3367-446f-9d65-0ae0ab539979" /> | <img width="340" height="420" alt="액션가면" src="https://github.com/user-attachments/assets/a357ad40-f772-4a96-a107-f3d056225dbe" /> | ![부리부리대마왕](https://github.com/user-attachments/assets/d0984d7d-e4da-4817-9ee3-61e1e1a0cb07) | <img width="438" height="398" alt="흰둥이" src="https://github.com/user-attachments/assets/09e80870-48c2-4b84-87b0-5f54523bd200" /> |
| 프로젝트 총괄 및 코드 병합 | 데이터 전처리 및 AWS | 시험지 및 답안 페이지 개발 | 메인 및 소개 페이지 개발 | 전체 페이지 개발 |

# 🧭기존 프로젝트 소개 (streamlit 버전)

기존 프로젝트 주소: https://github.com/skn-ai14-250409/SKN14-3rd-5Team

---

## 🎯 프로젝트 주제
**개인 맞춤형 AI 논술 과외 튜터 개발**

---

## 🔥프로젝트 소개
### 서비스명: 논스루(through)
LLM 기반의 RAG(Retrieval-Augmented Generation) 구조를 활용한 **대학 논술 첨삭 보조 시스템**입니다.
사용자가 작성한 논술 답안을 OCR 처리하고 이를 바탕으로 관련 문항의 채점 기준과 예시답안을 검색하고 분석하여, AI가 **구체적이고 구조적인 피드백**을 제공해줍니다. 또한, 사용자가 입력한 자신의 답안을 기반으로 **Q&A 챗봇** 기능도 지원하여, 자주 묻는 질문이나 구체적인 문장 단위의 피드백 요청도 가능합니다.


---

# 💡 이하 Django version

---

## 🧞 요구 사항 정의서


요구 사항 정의서는 01_requirements_spec/SKN14_4th_5Team_요구사항 정의서.pdf 로 대체

---

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


<img width="4988" height="2986" alt="skn14_4th_5team_system_architecture_with_white_background" src="https://github.com/user-attachments/assets/0f0e0195-95e8-4b7c-b917-7957c9494bf8" />



---

### 데이터 플로우


<img width="1828" height="830" alt="skn14_4th_5team_data_flow" src="https://github.com/user-attachments/assets/4f113cb3-4c7f-4ff4-a856-94bf15735bab" />

---

### 유저 플로우

<img width="1022" height="842" alt="skn14_4th_5team_user_flow" src="https://github.com/user-attachments/assets/3bdc5350-d960-48c8-a819-35aa7c6a11ee" />

---

## ✨ 구현 결과
|            구현 화면            | 역할                           | 
|:---------------------------:|:-----------------------------|
| <img width="1910" height="855" alt="index_home" src="https://github.com/user-attachments/assets/ce26296b-e7ed-42fb-95a7-d6c0f0ecacee" /> | 메인화면 |
| <img width="1286" height="820" alt="signup" src="https://github.com/user-attachments/assets/7f78f842-db5e-4291-8526-932b4a42f1f2" /> | 회원가입 / 로그인 화면 구현 |
| <img width="1494" height="819" alt="exam" src="https://github.com/user-attachments/assets/1026b011-8ac9-46f5-9bc0-4bb4dcf70bd7" /> | 시험지 보기 > 타이머 > 답안 제출하기 |
| <img width="1284" height="814" alt="gpting" src="https://github.com/user-attachments/assets/0aec116d-ddb9-402e-82ad-b7256578e3a1" /> | 답안 작성하기 > 답안 업로드 > GPT 첨삭 실행 |
| <img width="1906" height="850" alt="compare" src="https://github.com/user-attachments/assets/ad6eeb3b-d29c-4e54-b5ac-550fb00e5b18" /> |OCR 추출 > 내 답안과 모범답안 비교 |
| <img width="1258" height="430" alt="history" src="https://github.com/user-attachments/assets/e33f0c53-b1e3-4009-acfb-5807b6c3e060" /> | 첨삭 히스토리 제공 |
| <img width="1878" height="859" alt="result" src="https://github.com/user-attachments/assets/16d33ef6-f779-4be7-8967-852517a53d28" /> |첨삭 및 코멘트 확인|
| <img width="600" height="764" alt="chatbot" src="https://github.com/user-attachments/assets/6004f70d-83ff-407f-86ad-a0aa379e59ef" /> | 첨삭 관련 질문 및 FAQ 답변 확인 |

---

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

```cmd
"mysql.exe 경로"  -u root -p < setup.sql

*mysqlclient 없을 시
pip install mysqlclient
```


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


---

## 📝 회고록
*   **하종수:** html, css, js, django를 완전 처음 배우는데 역시 언어를 처음 배우는건 참 어려운 걸 다시금 깨달았습니다. 하지만 역시 재밌어요! 또한 AWS를 통해서 배포까지 해보고 싶었으나, 하지못한게 아쉬웠습니다. 다음엔 꼭... AWS를 이용해서 끝까지 완성을..! 그리고 역시나 우리 팀원들이 다들 열심히 해주셔서 너무 감사합니다!

*   **김성민:** 대학 논술 대비를 위한 AI 자동 첨삭 시스템을 EC2 환경에서 Docker 기반으로 배포하는 것을 목표로 진행했고, 처음에는 로컬 환경에서 잘 동작하던 코드를 AWS에 옮기면서, 환경 변수 설정, Dockerfile과 docker-compose.yml 작성, 그리고 컨테이너 실행 과정에서 예상치 못한 문제를 여럿 마주했습니다. 고생한 팀원들 정말 감사하고 좋은 경험이였습니다.

*   **송유나:** 기술적, 기능적인 부분만 개발하다가, 내가 만든 기능을 사용자에게 친절하게 닿을 수 있는 방법을 고민하며 사용자 친화적인 화면을 구상하는 과정에서 많은 것을 새롭게 배웠습니다. 단순한 기능 구현을 넘어, 동기·비동기 처리와 자동화된 배포 등 DevOps 관점에서의 전 과정을 경험해보고 싶은 동기가 생긴 프로젝트였습니다. PM의 역할이 얼마나 중요한지 다시 한 번 느낄 수 있었고, 두 번 연속 함께한 팀원들과의 협업도 감사한 경험이었습니다!

*   **이나경:** 이번 프로젝트에서는 서비스 이용자에게 편리한 페이지를 만들기 위해 많은 노력을 해보았습니다. streamlit이라는 제한적인 환경에서만 웹을 구성해보다가 django를 이용해 직접 내 손으로 html과 css를 구성해보는 과정이 정말 재미있었습니다. 메인 페이지를 맡아 서비스 이용자에게 어떻게 하면 좋은 첫인상과 신뢰감을 가져다줄 수 있을지 많이 고민해보았던 시간이었습니다. 추후 기회가 된다면 배포까지 완성해보면 더할 나위 없이 좋을 것 같습니다. 많이 도와주고 격려해주신 팀원분들 정말 감사드립니다!

*   **이승혁:** 이번 프로젝트는 단순히 Streamlit 프로토타입을 Django로 전환하는 것을 넘어, 웹 개발의 전체적인 흐름을 깊이 있게 체험하는 귀중한 경험이었습니다. 특히 사용자 인증부터 데이터베이스 설계, 비동기 통신(AJAX)을 이용한 AI 챗봇 구현까지, 각 기능이 유기적으로 연결되는 과정을 통해 풀스택 개발의 진정한 재미를 느꼈습니다. 수많은 버그와 씨름하며 얻은 안정적인 코드 구조는 앞으로의 개발 여정에 든든한 자산이 될 것입니다. 좋은 팀원들의 열성적인 노력 덕택에 팀프로젝트가 잘 마무리될 수 있었습니다. 감사합니다.
