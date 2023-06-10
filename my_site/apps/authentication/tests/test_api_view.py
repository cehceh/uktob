from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from django.contrib.auth.hashers import make_password
from unittest.mock import patch

from ..models import CustomUser

from .factory import UserFactory

from faker import Faker

# Create your tests here.

class MyAPIViewTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_object = UserFactory.build()
        cls.user_saved = UserFactory.create()
        cls.client = APIClient()
        cls.signup_url = reverse('custom_register')
        # cls.faker_obj = Faker()

    def authenticate(self):
        self.client.post(
            reverse( 'custom_register'), {
                'username': 'Amr',
                'password': '@1234567',
            }                    
        )
        response = self.client.post(
            reverse( 'custom_login'), {
                'username': 'amr',
                'password': '@1234567',
            }
        )


    def test_if_data_is_correct_then_signup(self):
        # response = self.client.get(reverse( 'custom_register'), )
        signup_dict = {
            'username': 'Amr', 
            'password1': '@1234567',
            'password2': '@1234567',
        }
        
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        

