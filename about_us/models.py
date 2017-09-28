from __future__ import unicode_literals

from django.db import models

# Create your models here.

class AboutUsData(models.Model):
	content = models.CharField(max_length=1000, blank=True, null=True)