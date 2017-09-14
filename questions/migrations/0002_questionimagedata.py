# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-07 08:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionImageData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.QuestionData')),
            ],
        ),
    ]