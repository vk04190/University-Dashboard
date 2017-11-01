# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# for generating models import models from django.db
from django.db import models
# for creating hash password import uuid
import uuid


# after any changes in manage.py run this command to reflect change into database
# "python manage.py makemigrations"

# once you have your new migration files, you should apply them to your database to make sure they work as expected:
# 'python manage.py migrate'


# Signup UserModel Here
class UserModel(models.Model):
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=400)
    # these[created_on,updated_on] fields are auto creating
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)


class SessionToken(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    last_request_on = models.DateField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    # it create session token
    def create_token(self):
        self.session_token = uuid.uuid4()



