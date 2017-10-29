# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# after any changes in manage.py run this command to reflect change into database
# "python manage.py makemigrations"

# once you have your new migration files, you should apply them to your database to make sure they work as expected:
# 'python manage.py migrate'


# # Create your models here.
# class user(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=200)
#     phone = models.CharField(max_length=30)
#     verified_phone_no = models.BooleanField(default=False)
#     age = models.IntegerField(default=0)
#     created_on = models.DateField(auto_now_add=True)
#     updated_on = models.DateField(auto_now=True)


# Signup UserModel Here
class UserModel(models.Model):
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=400)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
