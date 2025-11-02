from django.db import models

# Create your models here.

class Todo(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  completed = models.BooleanField(default=False)
  user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='todos')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title

  class Meta:
    ordering = ['-created_at']