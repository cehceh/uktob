# from django.contrib.sites import requests
# from django.core.exceptions import ValidationError
from django.db.models import Q

from allauth.account.adapter import DefaultAccountAdapter

from apps.authentication.models import CustomUser


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.username = data.get('username')
        
        user.save()  
        print(
            'REQUEST.USER::', request.user, 
            'REQUEST.AUTH::', request.auth 
        )
        return user

