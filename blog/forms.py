from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from .models import Comment, Post
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _


class SignUPForm(UserCreationForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs = {'class':'form-control'}))
	password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs = {'class':'form-control'}))
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']
		labels ={'email':'Email'}
		widgets = {'username': forms.TextInput(attrs = {'autofocus':True,'class':'form-control'}),'first_name': forms.TextInput(attrs = {'class':'form-control'}),'last_name': forms.TextInput(attrs = {'class':'form-control'}),'email': forms.EmailInput(attrs = {'class':'form-control'})}

class LoginForm(AuthenticationForm):
	username = UsernameField(widget= forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(label =_("Password"),strip=False, widget=forms.PasswordInput(attrs = {'autocomplete':'current-password', 'class':'form-control'}))


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['name', 'email', 'body']

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'slug', 'intro', 'body']
		labels = {'intro': 'Introduction'}
		widgets = {'title': forms.TextInput(attrs={'class':'form-control'}), 'intro': forms.Textarea(attrs={'class':'form-control'}), 'slug': forms.TextInput(attrs={'class':'form-control'}), 'body': forms.Textarea(attrs={'class':'form-control'})}


