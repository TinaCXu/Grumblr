from django import forms
from django.forms.boundfield import BoundField
from django.contrib.auth.models import User
from .models import UserProfileInfo, UserPost, UserPics

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    verify_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    age = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    introduction = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control input-sm'}))


    def clean(self):
        #super(RegistrationForm, self).clean()
        cleaned_data = super().clean()
        password = cleaned_data['password']
        verify_password = cleaned_data['verify_password']

        if password != verify_password:
            raise forms.ValidationError('Make sure password match!')

class LoginForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username','password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'width':'253.33px'}),
        }

class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username','first_name','last_name','password','email')

class PostForm(forms.ModelForm):
    class Meta():
        model = UserPost
        fields = ('post',)
        widgets = {
            'post': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "What's new today? Share with Grumblrer!"}),
        }

class PersonalProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    introduction = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control input-sm'}))

class PersonalPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    verify_new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserPicsForm(forms.ModelForm):
    class Meta():
        model = UserPics
        fields = ('profile_pic',)
