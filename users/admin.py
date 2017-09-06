from django.contrib import admin

# Register your models here.
from users.models import *

class UserDataAdmin(admin.ModelAdmin):
    list_display = ["id", "name","mobile","email","college","modified", "created","last_question_answered"
    				,"last_question_timestamp"]

admin.site.register(UserData, UserDataAdmin)

class OtpDataAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "otp","verified" ]

admin.site.register(OtpData, OtpDataAdmin)

class FcmDataAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "fcm" ]

admin.site.register(FcmData, FcmDataAdmin)
