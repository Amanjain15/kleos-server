from __future__ import unicode_literals

import datetime
from django.db import models
from college.models import *

# Create your models here.
	
class UserData(models.Model):
	name = models.CharField(max_length=255, blank=False, null=False)
	password = models.CharField(max_length=255, blank=False, null=False)
	mobile = models.CharField(max_length=255, unique=True, blank=False, null=True, default="")
	email = models.CharField(max_length=255, blank=True, null=True, default="")
	college = models.CharField(max_length=255, blank=False, null=True, default="")
	modified = models.DateTimeField(auto_now=True, auto_now_add=False)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	last_question_answered = models.IntegerField(default=0)
	last_question_timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.mobile

class OtpData(models.Model):
	user=models.ForeignKey(UserData)
	otp = models.IntegerField(blank=False, null=False)
	verified = models.BooleanField(default=False)

class FcmData(models.Model):
	user = models.ForeignKey(UserData)
	fcm = models.CharField(max_length=255, blank=False, null=False)