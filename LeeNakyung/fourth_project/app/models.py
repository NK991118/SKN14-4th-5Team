from django.db import models
from django.contrib.auth.models import User

class Submission(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.CharField(max_length=100)
    student_answer = models.TextField()
    ai_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'submission'
    def __str__(self):

        return f"{self.user.username} 학생의 {self.question_id} 제출"