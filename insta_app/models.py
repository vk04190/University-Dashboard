# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=30)
    verified_phone_no = models.BooleanField(default=False)
    age = models.IntegerField(default=0)
    created_on = models.DateField(auto_now_add=True)
