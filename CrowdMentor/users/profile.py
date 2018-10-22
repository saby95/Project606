from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from decimal import Decimal

from UserRoles import UserRoles


class Profile(models.Model):
    class Meta:
        app_label = 'users'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    role = models.CharField(max_length=15, choices=[(tag.value, tag.value) for tag in UserRoles], default=UserRoles.WORKER.value)
    performance = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    audit_prob_user = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    mentor = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='mentor')
    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
