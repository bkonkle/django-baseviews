from django.conf.urls.defaults import *

urlpatterns = patterns('test_project.views',
    url(r'^lol/$', 'LolHome'),
    url(r'^ajax/$', 'StrongerThanDirt'),
    url(r'^kitteh/$', 'KittehView'),
    url(r'^monorail/$', 'MonorailCatTicketsView'),
)
