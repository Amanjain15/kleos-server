from django.contrib import admin

# Register your models here.
from home.models import *


class TabDataAdmin(admin.ModelAdmin):
    list_display = ["tab_id", "title", "position"]

admin.site.register(TabData, TabDataAdmin)