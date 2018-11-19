from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from decimal import Decimal

from UserRoles import UserRoles

import datetime
from django.core.cache import cache
from django.conf import settings

class Profile(models.Model):
    class Meta:
        app_label = 'users'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=15, choices=[(tag.value, tag.value) for tag in UserRoles], default=UserRoles.WORKER.value)
    performance = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.05))
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.03))
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.02))
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    audit_prob_user = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(0.00))
    mentor = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='mentor', blank=True)

    def __str__(self):
        return str(self.user)

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                    seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
