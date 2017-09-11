from django.contrib import admin

# Register your models here.
from questions.models import *

class QuestionDataAdmin(admin.ModelAdmin):
	list_display= ["id","name","question_no","created",]


admin.site.register(QuestionData, QuestionDataAdmin)

class QuestionImageDataAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "image_url" ]

admin.site.register(QuestionImageData, QuestionImageDataAdmin)

class QuestionHintAdmin(admin.ModelAdmin):
	list_display = ["id", "question", "hint" ]
admin.site.register(QuestionHints, QuestionHintAdmin)	

class StoryDataAdmin(admin.ModelAdmin):
	list_display = ["id", "content", "image" ]
admin.site.register(StoryData, StoryDataAdmin)	