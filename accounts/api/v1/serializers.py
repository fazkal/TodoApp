from rest_framework import serializers
from  ...models import User,Profile
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255,write_only=True)

    class Meta:
        model = User
        fields = ['email','password','password1']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'detail':'password does not match'})
        
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('password1',None)
        return User.objects.create_user(**validated_data)
    

# Define serializer for resend token activation
class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"Details":"User does not exist"}
                )
        except User.is_verified:
            raise serializers.ValidationError(
                {"Details":"User is already activated and verified"}
                )
        attrs["user"] = user_obj
        return super().validate(attrs)
        

# Define serializer for change password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"Detail": "Passwords doesnt match"})
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return super().validate(attrs)
    
    
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email',read_only=True)
    class Meta:
        model = Profile
        fields = ('id','email','first_name','last_name','image','description')