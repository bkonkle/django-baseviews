from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^lol/$', 'test_project.views.LolHomeView'),
)
