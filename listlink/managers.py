from django.db import models
from utils.utils import link_generator
import hashlib
class ListLinkManager(models.Manager):
    def create_link(self,title,user,password=None):
        link=self.model(
            title=title,
            user=user,
            shorturl=link_generator(self.model)
        )
        if password is not None:
            link.password=hashlib.sha3_512(bytes(password,encoding='utf-8')).hexdigest()
        link.save()
        return link
    def delete_all_link(self,user):
        links=self.get_queryset().filter(user=user)
        for lin in links:
            for l2 in lin.addlink.all():
                l2.delete()
        links.delete()   

