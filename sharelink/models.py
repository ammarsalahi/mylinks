from django.db import models

class ShareLinkManager(models.Manager):
    def delete_all_link(self,user):
        links=self.get_queryset().filter(username=user)
        for lin in links:
            lin.link.delete()
        links.delete()
class ShareLink(models.Model):
    username=models.CharField(
        verbose_name='نام کاربری',
        max_length=300
    )
    link=models.ForeignKey(
        'link.Link',
        on_delete=models.CASCADE
    )
    title=models.CharField(
        max_length=2000,
        verbose_name='بدون عنوان',
        blank=True,
        null=True
    )
    created_at=models.DateTimeField(
        auto_now=True,
        verbose_name='زمان ایجاد'
    )
    persons=models.ManyToManyField(
        'user.User',
        verbose_name='کاربران',
        blank=True
    )  
    objects=models.Manager()
    obj=ShareLinkManager()