from django.contrib import admin
from .models import AdBlock, AdNetwork, CurrentAdNetwork

# Register your models here.

admin.site.register(AdBlock, admin.ModelAdmin)
admin.site.register(AdNetwork, admin.ModelAdmin)
admin.site.register(CurrentAdNetwork, admin.ModelAdmin)