from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TabData(models.Model):
	title = models.CharField(max_length=255, blank=True, null=True)
	position = models.IntegerField(null=False, blank=False,default=0)
	tab_id = models.IntegerField(null=False, blank=False,default=0)

	def __unicode__(self):
		return str(self.title)