from django.test import TestCase
from libxmApp.models import *




class UserProfileModelTest(TestCase):
    def test_create_user(self):
        email  = "test@example.com"
        username = "testuser"
        password = "testpassword"
        user_photo = "example.jpg"


        user = UserProfile.objects.create(email=email, username=username, password=password, user_photo=user_photo)
        return user

    def test_user_profile(self):
        w = self.test_create_user()
        self.assertTrue(isinstance(w,UserProfile))
        self.assertEqual(w.__str__(),w.username)

        

