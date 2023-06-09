from django.urls import path
from dj_rest_auth.views import LogoutView
# from .apis.views import TokenObtainPairView #, TokenRefreshView

from django.conf import settings

from .apis.views import (
    # DetailUserView,
    MyCustomRegister,
    MyCustomLogin,
    # TokenObtainPairView,
    UserTokenApi,
    # # CustomAuthToken,
    # TokenAPIView,
    SumListNum,
    ConcatenateStrings
)

urlpatterns = [    

    path('register/', MyCustomRegister.as_view(), name='custom_register'),
    path('login/', MyCustomLogin.as_view(), name='custom_login'),
    path('logout/', LogoutView.as_view()),
    
    path('sum/list/numbers/', SumListNum.as_view(), name='sum_list_num'),
    path('concatenate/two/strings/', ConcatenateStrings.as_view(), name='sum_list_num'),
    
    path('user/token/', UserTokenApi.as_view(), name='user_token'),
    
]

if getattr(settings, 'REST_USE_JWT', False):
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
        
    ]



