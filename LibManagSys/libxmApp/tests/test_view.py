from django.test import RequestFactory, TestCase
from django.utils import timezone
from django.template.response import TemplateResponse
from django.urls import reverse
from libxmApp.views import *
from libxmApp.models import *


class test_add_user(TestCase):

    def setUp(self):

        self.factory = RequestFactory()

    def test_add_user_success(self):

        self.client.login(username='testadmin', password='testpassword')


        url = reverse('add-user')

        data = {'userName': 'newuser', 'userPass': 'newpassword', 'userEmail': 'newuser@example.com'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)


        self.assertEqual(response.json()['result'], 'success')


        self.assertTrue(UserProfile.objects.filter(username='newuser').exists())

    def test_add_user_error(self):
        self.client.login(username='testadmin', password='testpassword')


        url = reverse('add-user') 

        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['result'], 'error')




