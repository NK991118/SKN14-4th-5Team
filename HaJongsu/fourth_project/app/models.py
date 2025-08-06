from django.db import models
from django.contrib.auth.models import User

class Submission(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.CharField(max_length=100)
    student_answer = models.TextField()
    ai_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'submission'  # 테이블 이름을 'submission'으로 설정
    def __str__(self):
        # 예: "홍길동 학생의 건국대 2023년 1번 문항 제출" 처럼 보이게 만들어줘.
        return f"{self.user.username} 학생의 {self.question_id} 제출"