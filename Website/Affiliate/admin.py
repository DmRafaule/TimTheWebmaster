from django.contrib import admin
from .models import AffiliateLink, AffiliateLinkConnectionSlug, AffiliateLinkConnectionTag, AffiliateLinkConnectionSpecial


admin.site.register(AffiliateLinkConnectionSlug, admin.ModelAdmin)
admin.site.register(AffiliateLinkConnectionTag, admin.ModelAdmin)
admin.site.register(AffiliateLinkConnectionSpecial, admin.ModelAdmin)
admin.site.register(AffiliateLink, admin.ModelAdmin)