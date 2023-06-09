from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Person(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    date_of_birth = models.DateField(default=None, null=True)
    age = models.PositiveIntegerField(default=None, null=True)
    username = models.CharField(max_length=100,blank=False, null=False, unique=True)
    password = models.CharField(max_length=100, blank=False, null=False)
