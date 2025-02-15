from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,PermissionsMixin,BaseUserManager)
from django.utils.translation import gettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):
    
    '''Custom user model manager when email is unique username'''
    def create_user(self,email,password, **extra_fields):
        if not email:
            raise ValueError(_("The email most be set"))
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Supervisor must have is_staff=True.'))
        if extra_fields.get('is_supervisor') is not True:
            raise ValueError(_('Supervisor must have is_supervisor=True.'))
        return self.create_user(email,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):

    '''Create custom user model'''
    email = models.EmailField(max_length=255, unique= True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_verified = models.BooleanField(default=False)
    # first_name = models.CharField(max_length=35)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]
    objects = UserManager()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email