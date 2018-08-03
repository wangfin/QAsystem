from django.db import models

# Create your models here.
class User(models.Model):
    userquestion = models.CharField(max_length=64)
    question_time = models.CharField(max_length=64)

class QuestionCount(models.Model):
    userquestion = models.CharField(max_length=64)
    questioncount = models.IntegerField()
