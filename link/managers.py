from  django.db import models
from utils.utils import link_generator

class LinkManager(models.Manager):
    def Create_Link(self,url,linktype):
        link=self.model(
            url=url,
            linktype=linktype,
            shorturl=link_generator(self.model)
        )
        link.save(self._db)
        return link