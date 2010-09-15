from django import forms
from baseviews.views import BasicView, AjaxView, FormView, MultiFormView


class LolHome(BasicView):
    template = 'home.html'
    
    def get_context(self):
        return {'verb': 'haz', 'noun': 'cheezburger'}


class StrongerThanDirt(AjaxView):

    def get_context(self):
        return {'armed': '...with Ajax!'}


class KittehForm(forms.Form):
    caption = forms.CharField()

    def save(self):
        pass


class KittehView(FormView):
    template = 'kitteh.html'
    form_class = KittehForm
    success_url = '/pewpewpew/'


class GoggieForm(forms.Form):
    bark = forms.CharField()

    def save(self):
        pass


class MonorailCatTicketsView(MultiFormView):
    template = 'monorail.html'
    form_classes = {'kitteh_form': KittehForm,
                    'goggie_form': GoggieForm}
    success_url = '/derailed/'
