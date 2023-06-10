from rest_framework import serializers, status
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase, TokenVerifyView

from dj_rest_auth.registration.views import RegisterView

from dj_rest_auth.views import LoginView
# from django.contrib.auth import authenticate

from apps.authentication.models import CustomUser
from .serializers import (
    UserTokenSerializer, 
    # ConcatenateStringsSerializer
)


class MyCustomLogin(LoginView):
    '''
        Managing login process
    '''

    def get_response(self):
        response = super(MyCustomLogin, self).get_response()

        #* here you can get specific fields in the login response 
        response.data['user'] = {
            'username': self.user.username,
        }
        # print('response:::', response.data)
        return response


class MyCustomRegister(RegisterView):
    '''
        Managing registration process
    '''
    def create(self, request, *args, **kwargs):    
        response = super(MyCustomRegister, self).create(request, *args, **kwargs)
        response.data['user'] = {
            'username': request.data['username'], 
        }
        
        return response



class UserTokenApi(APIView):

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data 

        user = CustomUser.objects.values('username')
        match = user.filter(id=request.user.id).exists()
        if match:
            obj = user.get(id=request.user.id)
        else:
            obj = [] 
        
        if obj == [] or obj['username'] != data['username']: # check for phone
            raise serializers.ValidationError({'error':'Incorrect user name'})

        # Generate Token
        refresh = RefreshToken.for_user(obj)

        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
                status=status.HTTP_200_OK
            )




#* For First Task
class SumListNum(APIView):
    
    def get(self, request, *args, **kwargs):
        """
            Calculates the sum of the list items
        """
        data_dict = {}
        my_arr = [25, '4443', 16, 15, 14, 13,] 
        data_dict['my_arr'] = my_arr
        check = [
            isinstance(item, int) for item in my_arr
        ]

        if False in check:
            result = Response(
                {'error': 'One or more item in your array are not a number'}, 
                status=status.HTTP_400_BAD_REQUEST)            
        else:
            sum_arr =  sum(my_arr)
            result = Response(
                {'Success, result is :' : sum_arr}, 
                status=status.HTTP_200_OK)
            
        return result
    


class ConcatenateStrings(generics.ListAPIView): 
    
    def get(self, request):
        """
            Concatenates two strings
        """
        data_dict = {}
        
        data_dict['str_one'] = 'Hello' 
        data_dict['str_two'] = request.user.username
        
        if  type(data_dict['str_one']) == str and type(data_dict['str_two']) == str:    
            data_dict['result'] = (data_dict['str_one']) + ' ' + (data_dict['str_two']) 
            result = Response(data_dict, status=status.HTTP_201_CREATED)
        else:
            result = Response(
                {'error': 'One of the variable or both of them are not String'}, 
                status=status.HTTP_400_BAD_REQUEST)
            
        return result
    