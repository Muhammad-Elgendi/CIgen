from django.db import models

# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     @property
#     def is_student(self):
#         return not (self.is_staff or self.is_superuser)

class Quiz(models.Model):
    name = models.CharField(max_length= 100)
    quiz = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name+' #'+str(self.id)

class Answer(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    answer = models.JSONField()
    created_at = models.DateTimeField()
    def __str__(self):
        return self.quiz.name+' @'+str(self.created_at)