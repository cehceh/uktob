from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import exceptions, serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from datetime import datetime, date

from django.core.validators import RegexValidator

from django.utils.timezone import utc
from django.contrib.auth import authenticate

from ..models import  CustomUser

import base64
from django.core.files.base import ContentFile



class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(max_length=20, required=False) # write_only=True
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    def validate_username(self, username):
        """
            :param username: The registered username
            :type username: str
            
            :return: username 
            
            :raises: `ValidationError`: if username already exists in the db

            check if username exists or not
        """

        try:
            user = CustomUser.objects.values('username')
            name = user.get(username=username)
            if name['username']:
                raise serializers.ValidationError(
                    ('This user name is already exist .....'),
                )

        # if no user registered 
        except ObjectDoesNotExist:
            return username

    
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['id'] = self.validated_data.get('id', '')
        data_dict['username'] = self.validated_data.get('username', '')
        # data_dict['last_name'] = self.validated_data.get('last_name', '')
        print(
            'data_dict::', data_dict 
            # 'data_dict::', 
        )
        
        return data_dict

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        """
            :param request: 
            :return: user 
            :make sure to assign user name 
        """
        user = super().save(request)
        
        user.username = self.data.get('username')
        user.save()
        
        return user


class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(label='User Name',required=True)
    # email = None

    def authenticate(self, **kwargs):
        """
            :param kwargs: 
            :type kwargs: dict
            
            :return: user 
            :type: User object
        """
        try:
            user = CustomUser.objects.get(username=kwargs['username'])
            if user.check_password(kwargs['password']):
                return user
        except ObjectDoesNotExist:
            return None
            
