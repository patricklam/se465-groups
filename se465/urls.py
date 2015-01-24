from django.conf.urls import patterns, url

from se465 import views

urlpatterns = patterns('',
    url(r'^1151/(?P<slug>\w+)/$', views.assignment, name='assignment'),
)
