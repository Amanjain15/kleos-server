from django.contrib import admin

# Register your models here.
from .models import *

class KeysDataAdmin(admin.ModelAdmin):
    list_display = ["key", "value", "modified", "created"]


admin.site.register(KeysData, KeysDataAdmin)

class WelcomeDataAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "quote"]

admin.site.register(WelcomeData,WelcomeDataAdmin)