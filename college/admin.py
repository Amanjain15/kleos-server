from django.contrib import admin

# Register your models here.
from college.models import *


class CollegeDataAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "modified", "created"]


admin.site.register(CollegeData, CollegeDataAdmin)