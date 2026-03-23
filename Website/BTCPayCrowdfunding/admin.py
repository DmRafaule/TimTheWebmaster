from django.contrib import admin
from .models import BTCPayCrowdfundApp, BTCPayCrowdfundDonation

# Register your models here.

admin.site.register(BTCPayCrowdfundApp, admin.ModelAdmin)
admin.site.register(BTCPayCrowdfundDonation, admin.ModelAdmin)