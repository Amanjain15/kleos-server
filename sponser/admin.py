from django.contrib import admin

# Register your models here.
from .models import *

class SponsorDataAdmin(admin.ModelAdmin):
    list_display = ["id", "name","image_url","url","content"]

admin.site.register(SponsorData, SponsorDataAdmin)