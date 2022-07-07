from django.db import models

class PrivateLinkManager(models.Manager):
    def delete_all_link(self,user):
        links=self.get_queryset().filter(user=user)
        for lin in links:
            lin.link.delete()
        links.delete()    
        
        
class PrivateLink(models.Model):
    link=models.ForeignKey(
        'link.Link',
        on_delete=models.CASCADE
    )
    user=models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE
    )
    title=models.CharField(
        verbose_name='عنوان',
        max_length=300,
        null=True,
        blank=True,
        default='بدون عنوان'
    )
    created_at=models.DateTimeField(
        auto_now=True
    )
    obj=PrivateLinkManager()
    objects=models.Manager()
    def get_link(self):
        return '127.0.0.1:8000/{}'.format(self.link.shorturl)  