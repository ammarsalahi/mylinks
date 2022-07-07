from django.db import models
from django.contrib.staticfiles.storage import staticfiles_storage
from biolink.managers import *

# Create your models here.
class BioLink(models.Model):
  
    user=models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE
    )
    social_media=models.ManyToManyField(
        'biolink.SocialMedia',
        verbose_name='شبکه اجتماعی',
        blank=True
    )
    title=models.CharField(
        verbose_name='نام یا عنوان',
        max_length=300
    )
    profile_image=models.ImageField(
        verbose_name='تصویر پروفایل',
        upload_to='profiles/bios/',
    )
    comment=models.TextField(
        verbose_name='توضیحات'
    )
    objects=models.Manager()
    obj=BioLinkManager() 
    def get_img(self):
        return self.profile_image.url


class SocialMedia(models.Model):
    choice_type=[
        ('Telegram','تلگرام'),
        ('Signal','سیگنال'),
        ('Instagram','اینستاگرام'),
        ('Linkedin','لینکدین'),
        ('Whatsapp','واتساپ'),
        ('Youtube','یوتیوب'),
    ]
    username=models.CharField(
        verbose_name='نام کاربری',
        max_length=300
    )
    typesocial=models.CharField(
        max_length=100,
        default='Telegram',
        verbose_name='نام شبکه اجتماعی',
        choices=choice_type
    )        
    def get_imgs(self):
        if self.typesocial=='Telegram':
            return staticfiles_storage.url('social/telegram.png')
        elif self.typesocial=='Instagram':
            return staticfiles_storage.url('social/instagram.png')
        elif self.typesocial=='Signal':
            return staticfiles_storage.url('social/signal.png')
        elif self.typesocial=='Linkedin':
            return staticfiles_storage.url('social/linkedin.png')
        elif self.typesocial=='Whatsapp':
            return staticfiles_storage.url('social/whatsapp.png')
        elif self.typesocial=='Youtube':
            return staticfiles_storage.url('social/youtube.png')    
    def get_urls(self):
        if self.typesocial=='Telegram':
            return 'https://telegram.me/{}'.format(self.username)
        elif self.typesocial=='Instagram':
            return 'https://instagram.com/{}'.format(self.username)
        elif self.typesocial=='Signal':
            return 'https://signal.com/{}'.format(self.username)
        elif self.typesocial=='Linkedin':
            return 'https://linkedin.com/{}'.format(self.username)
        elif self.typesocial=='Whatsapp':
            return 'https://whatsapp.com/{}'.format(self.username)
        elif self.typesocial=='Youtube':
            return 'https://youtube.com/{}'.format(self.username)
                
    



