from __future__ import unicode_literals

from django.db import models
# Create your models here.


class QuestionData(models.Model):
	name=models.CharField(max_length=255, blank=True, null=True)
	content=models.CharField(max_length=1000, blank=True, null=True)
	answer=models.CharField(max_length=255, blank=True, null=True)
	question_no=models.IntegerField(null=False,blank=False,default=0)
	created=models.DateTimeField(auto_now=False, auto_now_add=True)
	
	def __unicode__(self):
		return str(self.name)

class QuestionImageData(models.Model):
	question=models.ForeignKey(QuestionData)
	image_url=models.ImageField(upload_to='media/questions/',blank=True,null=True)


class QuestionHints(models.Model):
	question=models.ForeignKey(QuestionData)
	hint=models.CharField(max_length=1000, blank=True, null=True)

class StoryData(models.Model):
	content=models.CharField(max_length=3000, blank=True, null=True)
	image = models.ImageField(upload_to='media/story/',blank=True)

class BonusQuestionData(models.Model):
	name=models.CharField(max_length=255, blank=True, null=True)
	content=models.CharField(max_length=1000, blank=True, null=True)
	answer=models.CharField(max_length=255, blank=True, null=True)
	question_no=models.IntegerField(null=False,blank=False,default=0)
	created=models.DateTimeField(auto_now=False, auto_now_add=True)
	image_url=models.ImageField(upload_to='media/bonus_questions/',blank=True,null=True)

        def __unicode__(self):
                return str(self.name)


class BonusQuestionHints(models.Model):
	question=models.ForeignKey(BonusQuestionData)
	hint=models.CharField(max_length=1000, blank=True, null=True)
