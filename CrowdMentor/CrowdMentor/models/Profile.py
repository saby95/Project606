from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from CrowdMentor.utilities import UserRoles


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    role = models.CharField(max_length=15, choices=[(tag, tag.value) for tag in UserRoles], default=UserRoles.WORKER)
    performance = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    audit_prob_user = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    mentor_id = models.OneToOneField(User, on_delete=models.DO_NOTHING(), null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()