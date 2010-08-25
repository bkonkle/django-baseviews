from django.conf.urls.defaults import *
from baseviews import BasicView, view_factory

class LolHome(BasicView):
    template = 'home.html'
    cache_key = 'lol_home'
    cache_time = 60*20

    def cached_context(self):
        return {'verb': 'haz'}
        
    def uncached_context(self):
        return {'noun': 'cheezburger'}


urlpatterns = patterns('',
    url(r'^$', view_factory(LolHome)),
)
