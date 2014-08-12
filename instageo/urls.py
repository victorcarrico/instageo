from django.contrib import admin

from django.conf.urls import patterns, include, url

from instageo.photos.views import GeoPhotosView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', GeoPhotosView.as_view(), name='geo-photos'),
)
