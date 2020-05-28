from django.db import models
from django.contrib.auth.models import User
from django import template,templatetags
from django.utils import timezone

# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, default=None)
    introduction = models.TextField(max_length=420, blank=False, null=True, default='INTRODUCTION')
    age = models.CharField(max_length=3, blank=False, null=False, default=None)
    def __str__(self):
        return str(self.user)

class UserPost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    # username = models.CharField(max_length=500, blank=False, null=False)
    post = models.TextField(max_length=42, blank=True, null=True, default="")
    # post_pic = models.ImageField(upload_to='post_pics',blank=True)
    post_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)

class UserPics(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, default=None)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True,default='profile_pics/default.jpg')
    def __str__(self):
        return str(self.user)

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return f'{self.follower} follow {self.followed}'