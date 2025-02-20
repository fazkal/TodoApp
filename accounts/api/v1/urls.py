from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import (
   TokenObtainPairView, 
    TokenRefreshView,
    TokenVerifyView,
) 

app_name = "api-v1"

urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # activation
    path('activation/confirm/<str:token>', views.ActivationApiView.as_view(),name='activation'),

    # resend activation
    path('activation/resend/',views.ActivationResendApiView.as_view(),name='activation-resend'),

    # login jwt
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt-verify/', TokenVerifyView.as_view(), name='jwt-verify'),

    #change password
    path('change-password/',views.ChangePasswordApiView.as_view(), name='change-password'),

    #profile
    path('profile/',views.ProfileApiView.as_view(),name='profile'),
]