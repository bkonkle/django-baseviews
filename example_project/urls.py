from django.conf.urls.defaults import *
from baseviews import BasicView

from example_project.views import LolHome

urlpatterns = patterns('',
    url(r'^lol/$', LolHome),
    url(r'^rofl/$', "example_project.views.RoflHome"),
)
