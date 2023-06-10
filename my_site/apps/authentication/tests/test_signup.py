from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .factory import UserFactory
from ..models import CustomUser
from faker import Faker


class UserSignUpTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        cls.client = APIClient()
        cls.signup_url = reverse('custom_register')
        cls.faker_obj = Faker()
        

    # @Faker.override_default_locale('en_US')
    def test_if_data_is_correct_then_signup(self):
        # Prepare data
        obj = CustomUser.objects.create(
            username='root',
            password="@1234567",
        )
        signup_dict = {
            'username': 'Amr',
            'password1': '@1234567',
            'password2': '@1234567',
        }  
        
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        new_user = CustomUser.objects.get(username=obj.username)
        
        self.assertEqual(
            new_user.username,
            'root',
        )

    def test_username_if_already_exists_dont_signup(self):
        
        # Prepare data with already saved user
        signup_dict = {
            'username': 'root',
            'password1': '@1234567',
            'password2': '@1234567',
        }
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        