from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from user.managers import ActivationManager, UserManager
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

class User(AbstractBaseUser):
    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربران'
    username=models.CharField(
        unique=True,
        verbose_name='نام کاربری'
        ,max_length=200
    )
    fullname=models.CharField(
        null=True,
        blank=True,
        verbose_name='نام کامل'
        ,max_length=500
    )
    profile_image=models.ImageField(
        verbose_name='تصویر پروفایل',
        upload_to='user/profiles/',
    )

    email=models.EmailField(
        unique=True,
        verbose_name='ایمیل',
    )
    is_superuser=models.BooleanField(
        default=False,
    )
    is_staff=models.BooleanField(
        default=False
    )
    is_active_email=models.BooleanField(
        default=False
    )
    obj=UserManager()
    objects=models.Manager()
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email']

    def __str__(self):
        return self.username

    def has_perm(self,perm,obj=None):
        return self.is_superuser

    def has_module_perms(self,app_label):
        return True        

class Activation(models.Model):
    user=models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None
    )
    email=models.EmailField(
        verbose_name='ایمیل',
        blank=True,
        null=True
    )       
    active_code=models.CharField(
        verbose_name='کد',
        max_length=100
    )
    types=models.CharField(
        verbose_name='نوع',
        max_length=100
    )
    objects=models.Manager()
    obj=ActivationManager()
    
    def sendEmail(self,subs,request=None):
        email=''
        message=''
        if self.types=='register':
            message=render_to_string(
                template_name='user/message_reg.html',
                context={
                    'code':self.active_code
                }
            )
            email=self.email
        elif self.types=='forget':
            message=render_to_string(
                template_name='user/message_for.html',
                context={
                    'code':self.active_code,
                    'username':self.user.username,
                    'domain':get_current_site(request)
                }
            )
            email=self.user,email
        send_mail(
            subject=subs,
            message='',
            html_message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        ) 

class DeleteReason(models.Model):
    choice_type=[
        ('1','از سرویس راضی نیستم'),
        ('2','مشکل فنی داشت'),
        ('3','ظاهرش را نپسندیدم'),
        ('4','برای آزمایش از آن استفاده کردم'),
    ]
    reason=models.CharField(
        verbose_name='دلیل حذف حساب شما چیست؟',
        max_length=300,
        choices=choice_type
    )
    email=models.EmailField(
        verbose_name='ایمیل'
    )
    username=models.CharField(
        verbose_name='نام کاربری',
        max_length=300
    )
