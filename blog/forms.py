from django.contrib.auth.models import User
from django import forms
from .models import Post, Profile, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text','image') 




class UserForm(forms.ModelForm):
    #TODO: pwd with miniscule, maj, lettres et chiffres
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
        'placeholder': 'Your Password'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your name'}), 
        max_length=30,
        required=True )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Your E-mail'}),
        required=True,
        label= 'Your Email',

        max_length=75 )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':
        'Like #movies #kittens #travel #teacher #newyork'}), 
        max_length=30)
    class Meta:
        model = Profile
        fields = ('bio','location','avatar','cover','bd')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('textc',)