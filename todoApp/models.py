from django.db import models
from userApp.models import User

class Todo(models.Model):
  """ Todo Model Definition """
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField()
  content = models.TextField()
  is_checked = models.BooleanField(default=False)
  emoji = models.CharField(max_length=1, default="", blank=True)
  review = models.TextField(blank=True, default="")  # 리뷰 필드 추가
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.content
