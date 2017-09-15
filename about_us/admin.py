from django.contrib import admin

from .models import *
# Register your models here.
class AboutDataAdmin(admin.ModelAdmin):
    list_display = ["id", "content"]

admin.site.register(AboutUsData, AboutDataAdmin)