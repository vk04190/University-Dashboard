# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# html pages rendering and redirecting pages
from django.shortcuts import render, redirect
# import signup form from form.py
from forms import SignUpForm, SignInForm, PostForm, LikeForm, CommentForm
# importing library for password hashing and to check it
from models import UserModel, SessionToken, PostModel, LikeModel, CommentModel
from django.contrib.auth.hashers import make_password, check_password
# for using time zone and time related function
from datetime import datetime, timedelta
from django.utils import timezone
from smart_insta_clone.settings import BASE_DIR
# to save post on online data store using Imagur API
from imgurpython import ImgurClient
# IMGUR client Id and secret
My_CLIENT_ID = "b3b2ae95c944b54"
My_CLIENT_SECRET = "f67276a5cad94b2bc5cd7699ba936aab995a579f"

# Create your views here.
def signup_view(request):
    # if user send data to server['POST' request]
    if request.method == 'POST':
        # get the user post signup form details and clean data
        form = SignUpForm(request.POST)
        # validating input data in form
        if form.is_valid():
            # clean data to actual data to store in db
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # checking the different level of validation of data before save it into database
            if len(name) > 2 and len(email) > 7:
                # cheack wheather username at least 4 character
                if len(username) > 3:
                    # check wheather password must be atleast 5 character
                    if len(password) > 4:
                        # saving data to data base
                        # make_password function used for hashing password and then save it into database
                        user = UserModel(name=name, username=username, email=email, password=make_password(password))
                        user.save()
                        sucess = 'Hi ' + user.name + '. !!! Your Account Created Successfully. !!! Now Please Sign In.'
                        return render(request, 'login.html', {'color': 'w3-teal w3-large', 'status': sucess})
                    else:
                        form = SignUpForm()
                        error = 'Password Must be at least 5 characters long. Please Try a New Password.'
                        return render(request, 'index.html', {'form': form, 'color': 'w3-red', 'status': error})
                else:
                    form = SignUpForm()
                    error = 'Username Must be at least 4 characters long. Please Try a New Password.'
                    return render(request, 'index.html', {'form': form, 'color': 'w3-red', 'status': error})
            else:
                form = SignUpForm()
                error = 'Name Or Email Id is Not Valid. Please try again...'
                return render(request, 'index.html', {'form': form, 'color': 'w3-red', 'status': error})
        else:
            form = SignUpForm()
            error = 'Sign Up Details are Not Valid. Please Try Again ...'
            return render(request, 'index.html', { 'form': form, 'color': 'w3-red', 'status': error})
    elif request.method == 'GET':
        form = SignUpForm()
        daily = datetime.now()
        return render(request, 'index.html', {'form': form, 'color': 'w3-green', 'status': 'Welcome to Inspire Me. Today is', 'special': daily})


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
                    # if password is valid it will create a sesson token for each user
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    # if password username is valid but password is not valid
                    wrong_password = "Password or Username is Invalid. Please try Again !!!"
                    return render(request, 'login.html', {'color': 'w3-red w3-large', 'status': wrong_password})
            else:
                # if no such username found
                wrong_password = "Username or Password  Is Invalid. Please try Again !!!"
                return render(request, 'login.html', {'color': 'w3-red w3-large', 'status': wrong_password})

    elif request.method == 'GET':
        form = SignInForm()
    response_data['form'] = form
    return render(request, 'login.html', response_data)


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None


# post_view controller
def post_view(request):
    # check wheather user is valid or not
    user = check_validation(request)
    if user:
        # if user demand for post form
        if request.method == 'GET':
            form = PostForm()
            return render(request, 'post.html', {'form': form})
        # if user send post data
        elif request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                # now save data into database
                post = PostModel(user=user, image=image, caption=caption)
                post.save()
                # save images into imgur my_CLIENT_ID = b3b2ae95c944b54 my_CLIENT_SECRET = f67276a5cad94b2bc5cd7699ba936aab995a579f
                client = ImgurClient(My_CLIENT_ID, My_CLIENT_SECRET)
                path = str(BASE_DIR + '/' + post.image.url)
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()
                msg = 'New Status "' + caption + '" Updated Successfully. You Can Upload More...'
                return render(request, 'post.html', {'color': 'w3-green', 'status': msg})
            else:
                msg = 'Input Only Valid Image and Text. Please Try Again ... '
                return render(request, 'post.html', {'color': 'w3-red', 'status': msg})

    else:
        return redirect('/login/')


# feed view controller
def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')



        # def feed_view(request):
        #     user = check_validation(request)
        #     if user:
        #         posts = PostModel.objects.all().order_by('-created_on')
        #         # for post in posts:
        #         #     existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
        #         #     if existing_like:
        #         #         post.has_liked = True
        #         return render(request, 'home.html', {'posts': posts})
        #     else:
        #         return redirect('/login')


# like_view controller
def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')


# Comment_View Controller
def comment_view(request):
    user = check_validation(request)
    if user:
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')