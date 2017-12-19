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

class BonusQuestionDataAdmin(admin.ModelAdmin):
	list_display= ["id","name","question_no","image_url","created"]
admin.site.register(BonusQuestionData, BonusQuestionDataAdmin)

class BonusQuestionHintAdmin(admin.ModelAdmin):
	list_display = ["id", "question", "hint" ]
<<<<<<< HEAD
admin.site.register(BonusQuestionHints, BonusQuestionHintAdmin)	
=======
admin.site.register(BonusQuestionHints, BonusQuestionHintAdmin)	
>>>>>>> 11e39a93abdf62bb36736f267a9e52f385bd17ed
