from django.conf import settings
from django.test import TestCase, Client


if settings.ROOT_URLCONF == 'example_project.urls':
    # Only test against the example project
    
    class BaseviewTests(TestCase):
            
        def test_response(self):
            response = self.client.get("/lol/")

            self.assertEqual(response.content, 'I can haz cheezburger\n')

            self.assert_('verb' in response.context)
            self.assertEqual(response.context['verb'], 'haz')

            self.assert_('noun' in response.context)
            self.assertEqual(response.context['noun'], 'cheezburger')

            self.assertEqual(response.template.name, 'home.html')
            
            self.assertEqual(response['Content-Type'],
                             settings.DEFAULT_CONTENT_TYPE)
