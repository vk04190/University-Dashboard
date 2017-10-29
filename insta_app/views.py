# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render
from models import UserModel
# import signupform from form.py
from forms import SignUpForm
# importing library for password hashing
from django.contrib.auth.hashers import make_password


# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # print "SignUp Form Submitted"
        # validating input data in form
        if form.is_valid():
            # clean data to actual data to store in db
            name= form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to data base
            user = UserModel(name=name, username=username, email=email, password=make_password(password))
            user.save()
            sucess = 'Your Account Created Successfully. Now Please Sign'
            return render(request, 'login.html', {'sucess': sucess})
        else:
            form = SignUpForm()
            return render(request, 'index.html', {'form': form})
    elif request.method == 'GET':
        form = SignUpForm()
        daily = datetime.now()
        return render(request, 'index.html', {'form': form, 'today': daily})


def signin_view(request):
    return render(request, 'login.html')

