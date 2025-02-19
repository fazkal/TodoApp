from rest_framework import generics
from .serializers import (RegistrationSerializer,ChangePasswordSerializer,
                          ProfileSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from ...models import Profile
from django.shortcuts import get_object_or_404

User=get_user_model()

# Define class for registration user 
class RegistrationApiView(generics.GenericAPIView):
    serializer_class=RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data={
                'email':serializer.validated_data['email']
            }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

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