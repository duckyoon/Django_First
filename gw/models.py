from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


# Create your models here.

class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(default=now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True, blank=True) # 수정 일시 추가, null 허용, 값 없어도 허용
    
    def __str__(self):
        return self.subject
    
class Answer(models.Model):
    # Question모델의 속성에 연결하기 위해 Foreignkey 사용 및
    # 연결된 question이 삭제되면 answer도 삭제되게 설정
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(default=now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True, blank=True) # 수정 일시 추가, null 허용, 값 없어도 허용