"""grumblr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from post_app import views

urlpatterns = [
    path('',views.HomeView,name='home'),
    path('registration/',views.RegisterView,name='registration'),
    path('login/',views.LoginView,name='login'),
    path('logout/',views.logoutView,name='logout'),
    path('global/',views.PostView,name='global'),
    path('update_post/<str:timestamp>',views.UpdatePostView,name='update_post'),
    path('update_personal/<str:target_user>/<str:timestamp>', views.UpdatePersonalView,name='update_personal'),
    path('personal/<str:userID>',views.PersonalView,name='personal'),
    path('personal_profile/',views.PersonalProfileView,name='personal_profile'),
    path('personal_profile/update/',views.PersonalProfileFormView,name='personal_form'),
    path('personal_profile/update/<str:userID>',views.PersonalProfileUpdateView,name='personal_update'),
    path('follow/',views.FollowView,name='follow'),
    path('user_followed/',views.UserFollowedView,name='user_followed'),
    re_path(r'post_app/media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    path('admin/', admin.site.urls),
]
