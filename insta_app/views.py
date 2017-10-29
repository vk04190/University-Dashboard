# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
# html pages rendering and redirecting pages
from django.shortcuts import render, redirect
from models import UserModel, SessionToken #PostModel
# import signupform from form.py
from forms import SignUpForm, SignInForm #PostForm
# importing library for password hashing and to check it
from django.contrib.auth.hashers import make_password, check_password
# for using time zone and time related function
from datetime import timedelta
from django.utils import timezone


# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # validating input data in form
        if form.is_valid():
            # clean data to actual data to store in db
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to data base
            user = UserModel(name=name, username=username, email=email, password=make_password(password))
            user.save()
            sucess = 'Hi ' + user.name + ' Your Account Created Successfully. Now Please Sign'
            return render(request, 'login.html', {'status': sucess})
        else:
            form = SignUpForm()
            return render(request, 'index.html', {'form': form})
    elif request.method == 'GET':
        form = SignUpForm()
        daily = datetime.now()
        return render(request, 'index.html', {'form': form, 'today': daily})


def login_view(request):
    response_data = {}
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = UserModel.objects.filter(username=username).first()
            if user:
                # now check for password is true or not
                if check_password(password, user.password):
                    print 'password mating'
                    # if password is valid it will create a sesson token for each user
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('home/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    print "User Is Valid Sign In Successful"
                    return response
                else:
                    wrong_password = "Password Is Invalid. Please try Again !!!"
                    return render(request, 'login.html', {'status': wrong_password})
            else:
                wrong_password = "Username Is Invalid. Please try Again !!!"
                return render(request, 'login.html', {'status': wrong_password})

    elif request.method == 'GET':
        form = SignInForm()
    response_data['form'] = form
    return render(request, 'login.html', response_data)


def feed_view(request):
    return render(request, 'home.html')


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None
