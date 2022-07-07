from  django.db import models
from django.db.models.fields import URLField
from link.managers import LinkManager
from utils.utils import link_generator
from utils.choices import choice_u
from user.models import User

           
class Link(models.Model):
    url=models.URLField(
        verbose_name='آدرس'
    )
    shorturl=models.CharField(
        verbose_name='لینک نهایی',
        unique=True,
        max_length=200
    )
    linktype=models.CharField(
        max_length=100,
        verbose_name='نوع'
    )
    objects=models.Manager()
    obj=LinkManager()
    def get_shortlink(self):
        return self.shorturl        
        





