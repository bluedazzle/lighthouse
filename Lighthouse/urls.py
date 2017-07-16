from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps import views

import settings
from Lighthouse.sitemaps import ArticleSitemap

sitemaps = {
    'article': ArticleSitemap,
}

urlpatterns = [
    # Examples:
    # url(r'^$', 'Lighthouse.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('page.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap.xml', include('static_sitemaps.urls')),
    # url(r'^sitemap.xml$', views.index, {'sitemaps': sitemaps}),
    # url(r'^sitemap-(?P<section>.+)\.xml$', views.sitemap, {'sitemaps': sitemaps},
        # name='django.contrib.sitemaps.views.sitemap'),
    url(r'^s/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_MEDIA}),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
