from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
# For sitemap
from django.contrib.sitemaps.views import sitemap
from Main.sitemaps import StaticSitemap
from Post.sitemaps import PostSitemap

sitemaps = {
    "articles": PostSitemap,
    "static": StaticSitemap,
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
]


urlpatterns += i18n_patterns(
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path('', include('Main.urls')),
    path('', include('Engagement.urls')),
    path('', include('Breadcrumbs.urls')),
    path('', include('Affiliate.urls')),
    path('', include('YandexAdManager.urls')),
    path('tools/', include('Apps.WYSIWYGEditor.urls')),
    path('tools/', include('Apps.ImageThief.urls')),
    path('tools/', include('Apps.LinkThief.urls')),
    path('tools/', include('Apps.TextThief.urls')),
    path('tools/', include('Apps.RSSAggregator.urls')),
    path('tools/', include('Apps.ShaderToy.urls')),
    path('', include('Post.urls')),
    path('', include('PagiScroll.urls')),
)

handler400 = "Main.views.bad_request"
handler403 = "Main.views.forbidden"
handler404 = "Main.views.page_not_found"
handler500 = "Main.views.server_error"

# This is needed for displaying images media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
