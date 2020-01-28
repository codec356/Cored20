# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.static import serve

admin.autodiscover()

app_name = "core"

urlpatterns = [
                  url(r'^sitemap\.xml$', sitemap,
                      {'sitemaps': {'cmspages': CMSSitemap}}),
                  url(r'^admin/', admin.site.urls),  # NOQA
                  path('', include('cms.urls')),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  url(r'^select2/', include('django_select2.urls')),
                  # url(r'^/tinymce/', include('tinymce.urls')),
                  # url(r'^grappelli/$', include('grappelli.urls')),
                  url(r'^summernote/', include('django_summernote.urls')),

              ] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
                      url(r'^media/(?P<path>.*)$', serve,
                          {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                  ] + staticfiles_urlpatterns() + urlpatterns
