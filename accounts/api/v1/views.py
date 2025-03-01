from rest_framework import generics
from .serializers import (RegistrationSerializer,ChangePasswordSerializer,
                          ProfileSerializer,ActivationResendSerializer,LoginSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from ...models import Profile
from django.shortcuts import get_object_or_404,render,redirect
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import EmailThreading
import jwt
from django.conf import settings
from django.contrib.auth import login,logout
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from jwt.exceptions import ExpiredSignatureError,InvalidSignatureError

User=get_user_model()

# Define class for registration users and send mail with token for them 
class RegistrationApiView(generics.GenericAPIView):
    serializer_class=RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data = {'email':email}
            user_obj = get_object_or_404(User,email=email)
            token = self.get_token_for_user(user_obj)
            email_obj = EmailMessage('email/verify.tpl',{'token':token},
                                     'test4mydev@gmail.com',to=[email])
            EmailThreading(email_obj).start()
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get_token_for_user(self,user):
        Refresh = RefreshToken.for_user(user)
        return str(Refresh.access_token)


# Define class for activation users and verified them
class ActivationApiView(APIView):

    def get(self,request,token,*args,**kwargs):
        try:
            token = jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except ExpiredSignatureError:
            return Response({"Details":"Token has been expired"},
                            status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({"Details":"Token is not valid"},
                            status=status.HTTP_400_BAD_REQUEST)
        user_obj = User.objects.get(pk=user_id)

        if user_obj.is_verified:
            return Response ({"Details":"Your account has already been verified"})
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"Detail":"Your account have been verified and activated successfully"}
        )


# Define class for resend token activation via email to users
class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self,request,*args,**kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        token = self.get_token_for_user(user_obj)
        email_obj = EmailMessage("email/verify",{"token":token},
                                 "test4mydev@gmail.com",to=[user_obj.email],)
        EmailThreading(email_obj).start()
        return Response(
            {"Details":"User activation resend successfully"},
            status=status.HTTP_200_OK
        )

    def get_token_for_user(self,user):
        Refresh = RefreshToken.for_user(user)
        return str(Refresh.access_token)
    

# Define class for customize login user
class CustomLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def get(self,request,*args,**kwargs):
        return render(request,'accounts/login.html')

    def post(self, request, *args, **kwargs):
        """
        Login view to get user credentials
        """
        serializer = self.serializer_class(data=request.data, many=False)

        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            if user is not None and user.is_active:
                login(request, user)

                # return Response(serializer.data, status=status.HTTP_200_OK)
                #return redirect('/')
                return JsonResponse({'success': True, 'redirect_url': '/'}, status=status.HTTP_200_OK)

            return render('accounts/login.html',{'error':'Username or password is wrong or inactive'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     

# Define class for customize logout user
class LogoutApiView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        """
        Logout class
        """
        logout(request)
        return Response(
            {"non_field_errors": "successfully logged out"},
            status=status.HTTP_200_OK,
        )


# Define class for change password
class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    
    def get_object(self,queryset=None):
        obj = self.request.user
        return obj
    
    def put(self,request,*args,**kwargs):
        self.object = self.get_object()
        serializer=self.get_serializer(data= request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["wrong password"]},status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'details': 'Password changed successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

# Define class for set user profile info
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,user=self.request.user.id)
        return obj