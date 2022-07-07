from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from utils.utils import getcodeurl, getcode

class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if not username:
            raise ValueError('username!')
        if not email:
            raise ValueError('email!')
        user=self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,email,password=None):
        user=self.create_user(
            username=username,
            email=email,
            password=password
        ) 
        user.is_superuser=True 
        user.is_staff=True 
        user.save()
        return user

    def create_staffuser(self,username,email,password=None):
        user=self.create_user(
            username=username,
            email=email,
            password=password
        ) 
        user.is_staff=True 
        user.save()
        return user 
    def create_publicuser(self,username,password,fullname,profile_image,email=None,phone=None):
        user=self.create_user(
            username=username,
            email=email,
            password=password
        )
        if profile_image is not None:
            user.profile_image=profile_image
        user.fullname=fullname    
        user.phone=phone
        user.save()
        return user

class ActivationManager(models.Manager):
    def create_register(self,email):
        activation=self.model(
            types='register',
            active_code=getcode(),
            email=email,
            user=None
        ) 
        activation.save(using=self._db)
        return activation
    def create_forget(self,user):
        activation=self.model(
            types='forget',
            active_code=getcodeurl(),
            user=user
        )
        activation.save(using=self._db)
        return activation


