from django.conf import settings
from django.db import models
from oidc_provider.models import Client


class RpInfo(models.Model):
    client = models.OneToOneField(Client, models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='rps',
    )
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'RP {} for {}'.format(self.client, self.user)

    class Meta:
        verbose_name = 'relaying party detail'
        verbose_name_plural = 'relaying parties details'
