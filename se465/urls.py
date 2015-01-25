from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from se465 import views

urlpatterns = patterns('',
    url(r'^1151/(?P<slug>\w+)/$', views.assignment, name='assignment'),
    url(r'^login/$', 'django_cas.views.login', name='login'),
    url(r'^logout/$', 'django_cas.views.logout', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
