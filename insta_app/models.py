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


# class model sessontoken for generationg sesson token
class SessionToken(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    last_request_on = models.DateField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    # it create session token
    def create_token(self):
        self.session_token = uuid.uuid4()


# Post Model for handaling post data
class PostModel(models.Model):
    user = models.ForeignKey(UserModel)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # Like Counter
    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post=self))

    # comments show
    @property
    def comments(self):
        return CommentModel.objects.filter(post=self).order_by('-created_on')


# LikePost Model here
class LikeModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


# Comment Model
class CommentModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    comment_text = models.CharField(max_length=555)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)