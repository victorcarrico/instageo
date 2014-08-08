from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'instageo.views.home', name='home'),
    url(r'^', 'instageo.photos.views.index', name='index'),

    #url(r'^admin/', include(admin.site.urls)),
)
