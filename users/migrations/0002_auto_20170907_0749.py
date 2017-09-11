# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-07 07:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='last_question_timestamp',
        ),
        migrations.AlterField(
            model_name='userdata',
            name='last_question_answered',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.QuestionData'),
        ),
    ]
