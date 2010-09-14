from django.conf.urls.defaults import *

from example_project.views import LolHomeView

urlpatterns = patterns('',
    url(r'^lol/$', LolHomeView),
)
