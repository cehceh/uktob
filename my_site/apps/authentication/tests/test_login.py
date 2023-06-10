from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.authentication.models import CustomUser


class SignInViewTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='root',
            password="@1234567",
        )
        self.user.save()
        self.url = reverse('custom_login')

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        response = self.client.post(self.url, {'username': 'root', 'password': '@1234567'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_wrong_username(self):
        response = self.client.post(reverse('custom_login'), {'username': 'bogy', 'password': '@1234567'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_wrong_password(self):
        response = self.client.post(
            reverse('custom_login'), {'username': 'root','password': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        