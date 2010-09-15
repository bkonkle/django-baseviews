import unittest
from django.conf import settings
from django.test import TestCase, Client
from django.utils import simplejson
from baseviews.views import BasicView


@unittest.skipIf(not settings.ROOT_URLCONF == 'test_project.urls',
                 'These tests will only work with the test project.')
class BaseviewTests(TestCase):

    def test_basic_view(self):
        response = self.client.get('/lol/')

        self.assertEqual(response.content, 'I can haz cheezburger\n')

        self.assertTrue('verb' in response.context)
        self.assertEqual(response.context['verb'], 'haz')

        self.assertTrue('noun' in response.context)
        self.assertEqual(response.context['noun'], 'cheezburger')

        self.assertEqual(response.template.name, 'home.html')

        self.assertEqual(response['Content-Type'],
                         settings.DEFAULT_CONTENT_TYPE)

    def test_ajax_view(self):
        response = self.client.get('/ajax/')

        # This should fail because it's not an Ajax request
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/ajax/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(simplejson.loads(response.content)['armed'],
                         '...with Ajax!')

    def test_form_view(self):
        from test_project.views import KittehForm

        response = self.client.get('/kitteh/')
        self.assertEqual(response.content, str(KittehForm()))

        response = self.client.post('/kitteh/',
                                    {'caption': "No, you can't haz a pony."})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1],
                         'http://testserver/pewpewpew/')

    def test_multi_form_view(self):
        from test_project.views import KittehForm, GoggieForm

        response = self.client.get('/monorail/')
        self.assertEqual(response.content,
                         ' '.join([str(KittehForm()), str(GoggieForm())]))
        
        response = self.client.post('/monorail/',
                                    {'caption': "Not yours.",
                                     'bark': 'Woof!'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1],
                         'http://testserver/derailed/')
