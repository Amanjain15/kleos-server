from __future__ import unicode_literals

from django.db import models

# Create your models here.
class SponsorData(models.Model):
	name = models.CharField(max_length=1000, blank=True, null=True)
	image_url=models.ImageField(upload_to='media/sponsors/',blank=True,null=True)
	url= models.CharField(max_length=1000, blank=True, null=True)
	content = models.CharField(max_length=1000, blank=True, null=True)
