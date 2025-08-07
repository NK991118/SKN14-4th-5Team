# c:/Workspaces/Personal_Anything/3rd_to_4th/fourth_project/app/models.py

from django.db import models
# ★★★ Django의 기본 User 모델을 가져와! '누가' 제출했는지 연결하기 위해 필요해. ★★★
from django.contrib.auth.models import User

# 'Submission'이라는 이름의 데이터베이스 테이블 설계도를 만들 거야.
# models.Model을 상속받아야 Django가 모델로 인식해.
class Submission(models.Model):
    # -----------------
    # 1. 연결 정보 (누가?)
    # -----------------
    # user 필드: 이 제출물이 어떤 사용자의 것인지를 연결해주는 '꼬리표' 같은 거야.
    # ForeignKey는 다른 테이블(여기서는 User 테이블)의 특정 데이터와 연결하라는 뜻.
    # on_delete=models.CASCADE는 "만약 이 사용자가 탈퇴하면, 그가 작성한 모든 첨삭 기록도 함께 삭제된다"는 중요한 규칙이야.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # -----------------
    # 2. 문제 정보 (무엇을?)
    # -----------------
    # question_id 필드: 어떤 문제를 풀었는지 식별하기 위한 ID를 저장해. (예: 'konkuk_2023_1')
    # CharField는 글자 수를 제한하는 문자열 필드야. max_length는 필수 옵션!
    question_id = models.CharField(max_length=100)

    # -----------------
    # 3. 내용 (어떻게?)
    # -----------------
    # student_answer 필드: OCR로 추출된 학생의 답안 텍스트를 저장해.
    # TextField는 글자 수 제한이 없는 긴 텍스트를 위한 필드야. 답안은 길 수 있으니까!
    student_answer = models.TextField()
    
    # ai_comment 필드: AI가 생성해준 첨삭 코멘트 전체를 저장해.
    # 이것도 매우 길 수 있으니 TextField를 사용해.
    ai_comment = models.TextField()

    # -----------------
    # 4. 시간 정보 (언제?)
    # -----------------
    # created_at 필드: 이 기록이 언제 생성되었는지 시간을 저장해.
    # DateTimeField는 날짜와 시간을 모두 저장하는 필드야.
    # auto_now_add=True 옵션은, 이 데이터가 처음 만들어지는 그 순간의 시간을 자동으로 저장해주는 마법 같은 기능이야.
    created_at = models.DateTimeField(auto_now_add=True)

    # -----------------
    # (보너스) 관리자 페이지에서 보기 좋게 표시하기 위한 설정
    # -----------------
    # 이 함수는 Submission 객체를 사람이 알아보기 좋은 문자열로 표현해주는 역할을 해.
    # 이게 없으면 관리자 페이지에서 'Submission object (1)', 'Submission object (2)'처럼 보여서 뭐가 뭔지 알 수가 없어.
    def __str__(self):
        # 예: "홍길동 학생의 건국대 2023년 1번 문항 제출" 처럼 보이게 만들어줘.
        return f"{self.user.username} 학생의 {self.question_id} 제출"