from __future__ import unicode_literals

import datetime
from django.db import models
from college.models import *
from questions.models import QuestionData
# Create your models here.
	
class UserData(models.Model):
	name = models.CharField(max_length=255, blank=False, null=False)
	password = models.CharField(max_length=255, blank=False, null=False)
	mobile = models.CharField(max_length=255, unique=True, blank=False, null=True, default="")
	email = models.CharField(max_length=255, blank=True, null=True, default="")
	college = models.CharField(max_length=255, blank=False, null=True, default="")
	modified = models.DateTimeField(auto_now=True, auto_now_add=False)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	last_question_answered = models.ForeignKey(QuestionData, null = True, blank=True)
	last_question_timestamp = models.DateTimeField(null=True,blank=True)

	def __unicode__(self):
		return self.mobile

class OtpData(models.Model):
	user=models.ForeignKey(UserData)
	otp = models.IntegerField(blank=False, null=False)
	verified = models.BooleanField(default=False)

class FcmData(models.Model):
	user = models.ForeignKey(UserData)
	fcm = models.CharField(max_length=255, blank=False, null=False)

class UserQuestionData(models.Model):
	user = models.ForeignKey(UserData)
	question = models.ForeignKey(QuestionData)
	answered = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

# class UserScoreData(models.Model):
# 	user=models.ForeignKey(UserData)
# 	rank=models.IntegerField(null=False,blank=False,default=0)