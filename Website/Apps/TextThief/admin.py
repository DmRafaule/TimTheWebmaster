from django.contrib import admin
from .models import TextThiefRecord



admin.site.register(TextThiefRecord, admin.ModelAdmin)