from django.contrib import admin
from .models import YandexAdBlock, YandexAdLocation, YandexAdBlockConfiguration, YandexCurrentAdBlockConfiguration

# Register your models here.

admin.site.register(YandexAdBlock, admin.ModelAdmin)
admin.site.register(YandexAdLocation, admin.ModelAdmin)
admin.site.register(YandexAdBlockConfiguration, admin.ModelAdmin)
admin.site.register(YandexCurrentAdBlockConfiguration, admin.ModelAdmin)