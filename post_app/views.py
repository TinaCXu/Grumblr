from django.shortcuts import render, get_object_or_404
from post_app import forms
from .models import UserProfileInfo, User, UserPost, UserPics, Follow
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.forms.boundfield import BoundField
from django.core import serializers

from datetime import datetime
from datetime import timedelta

import json

# Create your views here.

def HomeView(request):
    return render(request,'home.html')

#GET request: user want a html
#POST  request: user want to send data to server

def RegisterView(request):

    if request.method == "GET":
        register_form = forms.RegisterForm()
        #isolate the dictionary-context from function render, incase there are lots of key and value
        context = {}
        context['register_form'] = register_form
        return render(request,'registration.html',context)
        
    #if we are here, the request must be post
    if request.method == 'POST':
    #if it is post, user is submitting info by form.
        #step 1 get the form
        register_form = forms.RegisterForm(data=request.POST)
        #step 2 see if it is valid
        if register_form.is_valid():
            #it is valid, store it into the database
            user = User()
            user.username = register_form.cleaned_data['username']
            user.first_name = register_form.cleaned_data['first_name']
            user.last_name = register_form.cleaned_data['last_name']
            user.password = register_form.cleaned_data['password']
            user.email = register_form.cleaned_data['email']
            user.set_password(user.password) #hashing the password

            # u = User.objects.get(username=user.username)
            # user_profile.introduction

            user.save()

            user_profile = UserProfileInfo()
            user_profile.introduction = register_form.cleaned_data['introduction']
            user_profile.age = register_form.cleaned_data['age']
            user_profile.user = user
            user_profile.save()
            return HttpResponse("register success")
        #step 3 if it is not valid, return information
        else:
            context = {}
            context['register_form'] = register_form
            return render(request,'registration.html',context)
    return HttpResponse("404")

def LoginView(request):
    if request.method == "GET":
        login_form = forms.LoginForm()
        #isolate the dictionary-context from function render, incase there are lots of key and value
        context = {}
        context['login_form'] = login_form
        return render(request,'login.html',context)

    if request.method == 'POST':
    #if it is post, user is submitting info by form.
        #step 1 get the form
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        #step 2 see if it is valid
        if user is not None:
            # A backend authenticated the credentials
            login(request,user)
            return HttpResponseRedirect(reverse('global'))
            # success page should be linked to personal page, specify it tomorrow
        return render(request,'login.html',context)
    return HttpResponse("404")

@login_required
def logoutView(request):
    logout(request)
    return render(request,'home.html')

@login_required
def PostView(request):
    if request.method == 'GET':
        post_form = forms.PostForm
        post_list = UserPost.objects.order_by('-post_time')
        context = {}
        context['post_form'] = post_form
        context['post_records'] = post_list
        return render(request,'global_stream.html',context)
    if request.method == 'POST':
        #if it is post, user is submitting info by form.
        #step 1 get the form
        #3 fields, post is provided by request.POST
        # user and time is provided by instance post, use instance to add it to post_form
        post = UserPost(user=request.user)
        post_form = forms.PostForm(data=request.POST, instance=post)

        # updatepost = UpdatePost()
        # updatepost = request.POST['latest_post_time']
        # updatepost.save()

        #step 2 see if it is valid
        if post_form.is_valid():
            #it is valid, store it into the database
            post_form.save()            
            return HttpResponse("Post success")
        #step 3 if it is not valid, return information
        else:
            context = {}
            context['post_form'] = post_form
            return render(request,'global_stream.html',context)
    return HttpResponse("404")


def UpdatePostView(request, timestamp):
    print('UpdatePostView:', timestamp)
    if request.method == 'GET':
        #1. get posts newer than timestamp
        # TODO: order?:ok
        # TODO: gte? gt = great, gte = great or equal.
        # TODO: max time is a string of time. check if string is time.
        existing_posts = UserPost.objects.order_by('-post_time')
        print(str(existing_posts[0].post_time))
        print(type(existing_posts[0].post_time))

        print(timestamp)
        print(type(timestamp))

        if str(existing_posts[0].post_time) == timestamp:
            newest_posts={
                "timestamp": timestamp,
                "posts": "" 
            }
            return HttpResponse(json.dumps(newest_posts), content_type='application/json')
        else:
            newest_posts = UserPost.objects.filter(post_time__gt=timestamp).order_by('-post_time')
            # print(newest_post)
            print(len(newest_posts))
            print(newest_posts)
            print(newest_posts[0].user)
            print(newest_posts[0].post)
            print(newest_posts[0].post_time)
            print(newest_posts[0].user.id)

            newest_post_pool = []
            for i in range(len(newest_posts)):
                newest_post = {
                    "timestamp":(newest_posts[i].post_time+timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                    "user":newest_posts[i].user.username,
                    "post":newest_posts[i].post,
                    "user_id":str(newest_posts[i].user.id),
                    }
                newest_post_pool.append(newest_post)
            print(newest_post_pool)

            #2. return them and newest timestamp (json format)
            # TODO:last post is the newest post?
            newest_posts={
                "timestamp": str(newest_posts[0].post_time),
                "posts":  newest_post_pool
            }
            return HttpResponse(json.dumps(newest_posts), content_type='application/json')
    return HttpResponse("404")

@login_required
def PersonalView(request,userID):
    print('UpdatePersonalView:', userID)
    if request.method == 'GET':
        target_user = User.objects.get(id=userID)
        target_user_first_name = target_user.first_name
        target_user_last_name =target_user.last_name

        post_form = forms.PostForm
        post_list = UserPost.objects.filter(user=target_user).order_by('-post_time')
        introduction = get_object_or_404(UserProfileInfo,user=target_user).introduction       
        print(introduction)
        print(request.user.id)

        context = {}
        context['post_form'] = post_form
        context['post_records'] = post_list
        context['user_name'] = post_list[0].user
        context['user_introduction'] = introduction
        context['first_name'] = target_user_first_name
        context['last_name'] = target_user_last_name
        return render(request,'personal.html',context)

    if request.method == 'POST':
        #if it is post, user is submitting info by form.
        #step 1 get the form
        #3 fields, post is provided by request.POST
        # user and time is provided by instance post, use instance to add it to post_form
        post = UserPost(user=request.user)
        post_form = forms.PostForm(data=request.POST, instance=post)

        # updatepost = UpdatePost()
        # updatepost = request.POST['latest_post_time']
        # updatepost.save()

        #step 2 see if it is valid
        if post_form.is_valid():
            #it is valid, store it into the database
            post_form.save()            
            return HttpResponse("Post success")
        #step 3 if it is not valid, return information
        else:
            context = {}
            context['post_form'] = post_form
            return render(request,'global_stream.html',context)
    return HttpResponse("404")

def UpdatePersonalView(request, target_user, timestamp):
    print('UpdatePostView:', timestamp)
    if request.method == 'GET':
        existing_posts = UserPost.objects.filter(user=target_user).order_by('-post_time')
        print(str(existing_posts[0].post_time))
        print(type(existing_posts[0].post_time))

        print(timestamp)
        print(type(timestamp))

        if str(existing_posts[0].post_time) == timestamp:
            newest_posts={
                "timestamp": timestamp,
                "posts": "" 
            }
            return HttpResponse(json.dumps(newest_posts), content_type='application/json')
        else:
            newest_posts = UserPost.objects.filter(user=target_user,post_time__gt=timestamp).order_by('-post_time')
            # print(newest_post)
            print(len(newest_posts))
            print(newest_posts)
            print(newest_posts[0].user)
            print(newest_posts[0].post)
            print(newest_posts[0].post_time)
            print(newest_posts[0].user.id)

            newest_post_pool = []
            for i in range(len(newest_posts)):
                newest_post = {
                    "timestamp":(newest_posts[i].post_time+timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                    # "user":newest_posts[i].user.username,
                    "post":newest_posts[i].post,
                    # "user_id":str(newest_posts[i].user.id),
                    }
                newest_post_pool.append(newest_post)
            print(newest_post_pool)

            #2. return them and newest timestamp (json format)
            # TODO:last post is the newest post?
            newest_posts={
                "timestamp": str(newest_posts[0].post_time),
                "posts":  newest_post_pool
            }
            return HttpResponse(json.dumps(newest_posts), content_type='application/json')
    return HttpResponse("404")

@login_required
def PersonalProfileView(request):
    if request.method == 'GET':
        personal_profile = UserProfileInfo.objects.get(user=request.user)
        user_pics = UserPics.objects.get(user=request.user)
        print(personal_profile)
        print(personal_profile.introduction)
        print(personal_profile.age)
        print(user_pics.profile_pic)

        context = {}
        context['first_name'] = request.user.first_name
        context['last_name'] = request.user.last_name
        context['age'] = personal_profile.age
        context['introduction'] = personal_profile.introduction
        context['profile_pic'] = user_pics.profile_pic

        return render(request,'personal_profile.html',context)
    if request.method == 'POST':
        return HttpResponseRedirect('/personal_profile/update/')

@login_required
# static part for personal profile
def PersonalProfileFormView(request):
    if request.method == 'GET':
        # prepate the form skelton for html
        profile_form = forms.PersonalProfileForm()
        password_form = forms.PersonalPasswordForm()
        profile_pic_form = forms.UserPicsForm()
        context = {}
        context['profile_form'] = profile_form
        context['password_form'] = password_form
        context['profile_pic_form'] = profile_pic_form
        context['user_id'] = request.user.id

        return render(request,'personal_update.html',context)
    if request.method == 'POST':
        #three types of post, one is submitting PersonalProfileForm, one is submitting PersonalPasswordForm, one is submitting UserPicsForm
        if 'first_name' in request.POST:
            print(request.POST)
            print(type(request.POST))
            updated_profie = forms.PersonalProfileForm(request.POST)
            if updated_profie.is_valid():
                # 3 fields should be saved in model User, 2 fields should be saved in model UserProfileInfo
                updateUser_user = request.user
                print(updateUser_user)
                updateUser_user.first_name =  request.POST['first_name']
                updateUser_user.last_name =  request.POST['last_name']
                updateUser_user.email =  request.POST['email']
                updateUser_user.save(update_fields=['first_name','last_name','email'])

                user_profile = UserProfileInfo.objects.get(user=request.user)
                print(user_profile)
                user_profile.introduction = request.POST['introduction']
                user_profile.age = request.POST['age']
                user_profile.save(update_fields=['introduction','age'])
                return HttpResponse("profile update success")
            else:
                return HttpResponse("profile update fail")
        if 'old_password' in request.POST:
            print(request.POST)
            print(type(request.POST))
            updated_password = forms.PersonalPasswordForm(request.POST)
            if updated_password.is_valid():
                # step1:check old password is matched
                database_password = request.user.password #ciphertext
                old_password = request.POST['old_password'] #plaintext
                if check_password(old_password, database_password):
                    # step2:check new passwords are matched
                    new_password = request.POST['new_password']
                    verify_new_password = request.POST['verify_new_password']
                    if new_password == verify_new_password:
                        updateUser_user = request.user
                        updateUser_user.password =  new_password
                        updateUser_user.set_password(updateUser_user.password) #hashing the password
                        updateUser_user.save(update_fields=['password'])
                        return HttpResponse("Password update success!")
                    else:
                        return HttpResponse("Please make sure new password match")
                else:
                    return HttpResponse("Please make sure the old password match!")
        if 'profile_pic' in request.FILES:
            user_pics = UserPics.objects.get(user=request.user)
            user_pics.profile_pic = request.FILES['profile_pic']
            user_pics.save(update_fields=['profile_pic'])
            return HttpResponse("profile pic update success")


@login_required
# dynamic part for personal profile
def PersonalProfileUpdateView(request, userID):
    if request.method == 'GET':
        # prepare the initial form data for user
        personal_profile = UserProfileInfo.objects.get(user=request.user)
        personal_data = {
            "username":request.user.username,
            "first_name":request.user.first_name,
            "last_name":request.user.last_name,
            "email":request.user.email,
            "age":personal_profile.age,
            "introduction":personal_profile.introduction,
        }
        print(personal_data)
        # return the data to frontend
        return HttpResponse(json.dumps(personal_data), content_type='application/json')

@login_required
def FollowView(request, to_user):
    if request.method == 'POST':
        current_follow_status = Follow.objects.filter(follower=request.user, followed=to_user).all()
        # if follow
        if current_follow_status == False:
            follow_status = Follow()
            follow_status.follower = request.user
            follow_status.followed = to_user
            follow_status.save()
            return HttpResponse("Follow Success!")
        # if unfollow
        if current_follow_status == True:
            current_follow_status.delete()
            return HttpResponse("Unfollow Success!")

def UserFollowedView(request):
    if request.method == 'GET':
        followeders = Follow.objects.filter(follower=request.user).all()
        print(followeders)
        followed_list = []
        for followder in followeders:
            followed_list.append(str(followder.followed))
        print(followed_list)
        user_followed = {
            "followeder":followed_list
        }
        print(user_followed)
        # return HttpResponse(followed_list)
        # return JsonResponse(user_followed)
        return HttpResponse(json.dumps(user_followed), content_type='application/json')

