from django.db import models


class BioLinkManager(models.Manager):
    def delete_bio(self,user):
        bio=self.get_queryset().get(user=user)
        for social in bio.social_media.all():
            social.delete()
        bio.delete()  