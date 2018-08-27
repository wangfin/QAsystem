from django.db import models

# Create your models here.
class User(models.Model):
    userquestion = models.CharField(max_length=64)
    question_time = models.CharField(max_length=64)

class QuestionCount(models.Model):
    userquestion = models.CharField(max_length=64)
    questioncount = models.IntegerField()

class UserMining(models.Model):
    userip = models.CharField(max_length=100) # 用户ip
    userquestion = models.CharField(max_length=500) # 用户问题
    usersub = models.CharField(max_length=64) # 用户问题主题
    userattention = models.CharField(max_length=64) # 用户倾向（闲聊还是提问）
    # usercollect = models.NullBooleanField  # 用户是否有收藏这个QA
    userlike=models.IntegerField(null=True)  # 用户是否喜欢这个回答以及喜欢程度
    times = models.CharField(max_length=64,null=True) # 用户提问时间

