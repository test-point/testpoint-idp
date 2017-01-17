import json
import logging

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


class BusinessProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='business'
    )
    parent_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='subusers',
        blank=True, null=True
    )
    extra_data = models.TextField(blank=True, null=True, default=None)

    class Meta:
        verbose_name_plural = 'business profiles'
        ordering = ('user',)

    def __unicode__(self):
        return u"{}: {}".format(self.user, self.extra_data)

    def set_extra_data(self, data):
        assert isinstance(data, dict)
        self.extra_data = json.dumps(data)
        self.save()
        return

    def get_extra_data(self):
        extra_data = {}
        try:
            extra_data.update(json.loads(self.extra_data))
        except Exception as e:
            logging.exception(e)
        if 'abn' not in extra_data and self.parent_user_id is not None:
            extra_data['abn'] = self.user.username
        return extra_data

    def get_role_display(self):
        if self.user.is_superuser or self.user.is_staff:
            return 'Staff member'
        if not self.is_developer:
            return 'Synthetic user'
        return 'Developer'

    def get_readable_name(self):
        if self.user.first_name or self.user.last_name:
            return u"{} {}".format(self.user.first_name, self.user.last_name).strip()
        return self.user.username

    @property
    def is_developer(self):
        return self.parent_user is None

    @property
    def is_synthetic(self):
        return self.parent_user is not None


def create_profile(sender, **kwargs):
    instance = kwargs["instance"]
    if kwargs["created"]:
        BusinessProfile.objects.create(
            user=instance
        )
    return

models.signals.post_save.connect(create_profile, sender=User)
