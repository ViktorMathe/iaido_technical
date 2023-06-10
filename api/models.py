from django.db import models
from django.db.models.signals import post_save
from django.conf import settings


class Person(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    date_of_birth = models.DateField(default=None, null=True)
    age = models.PositiveIntegerField(default=None, null=True)
    username = models.CharField(max_length=100,blank=False, null=False, unique=True)
    password = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.username
