from django.db import models


class PublicLinkManager(models.Manager):
    def delete_all_link(self,user):
        links=self.get_queryset().filter(user=user)
        for lin in links:
            lin.link.delete()
        links.delete()   
class PublicLink(models.Model):
    link=models.ForeignKey(
        'link.Link',
        on_delete=models.CASCADE
    )
    user=models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True
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
    obj=PublicLinkManager()
    objects=models.Manager()
    def get_shortlink(self):
        return self.link.shortlink