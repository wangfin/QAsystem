# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class QuestionCount(models.Model):
    userquestion = models.CharField(max_length=64)
    questioncount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'QAManagement_questioncount'


class User(models.Model):
    userquestion = models.CharField(max_length=64)
    question_time = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'QAManagement_user'


class UserMining(models.Model):
    userip = models.CharField(max_length=100)
    userquestion = models.CharField(max_length=500)
    usersub = models.CharField(max_length=64)
    userattention = models.CharField(max_length=64)
    usercollect = models.CharField(max_length=64, blank=True, null=True)
    userlike = models.FloatField(blank=True, null=True)
    times = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'QAManagement_usermining'

