from baseviews.views import BasicView

class LolHomeView(BasicView):
    template = 'home.html'
    
    def get_context(self):
        return {'verb': 'haz', 'noun': 'cheezburger'}
