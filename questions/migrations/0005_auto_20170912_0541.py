# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-12 05:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_questionhints_storydata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionimagedata',
            name='image_url',
            field=models.ImageField(blank=True, null=True, upload_to='media/questions/'),
        ),
        migrations.AlterField(
            model_name='storydata',
            name='image',
            field=models.ImageField(blank=True, upload_to='media/story/'),
        ),
    ]