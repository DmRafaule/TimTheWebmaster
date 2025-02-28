from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
# For sitemap
from django.contrib.sitemaps.views import sitemap
from Post.models import PostSitemap
from Main.models import StaticSitemap
from PagiScroll.models import PaginationSitemap
#from Gallery.models import ImagesSitemap

sitemaps = {
    "articles": PostSitemap,
    "static": StaticSitemap,
}

sitemaps_pagination = {
    "pagination": PaginationSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "sitemap-pagination.xml",
        sitemap,
        {"sitemaps": sitemaps_pagination},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]


urlpatterns += i18n_patterns(
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path('', include('Main.urls')),
    path('', include('Admin.urls')),
    path('', include('Engagement.urls')),
    path('', include('Breadcrumbs.urls')),
    path('tools/', include('PostEditor.urls')),
    path('tools/', include('PagiScrollEditor.urls')),
    path('tools/', include('ImageThief.urls')),
    path('tools/', include('WebGLEngine.urls')),
    path('tools/', include('RSSAggregator.urls')),
    path('tools/', include('ShaderToy.urls')),
    path('', include('Post.urls')),
    path('', include('PagiScroll.urls')),
)

handler404 = "Main.views.page_not_found"

# This is needed for displaying images media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
