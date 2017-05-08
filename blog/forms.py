from django.contrib.auth.models import User
from django import forms
from .models import Post, Profile, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(widget=TinyMCE(attrs={'class': 'form-control'}))
    class Meta:
        model = Post
        fields = ('title', 'text','image') 




class UserForm(forms.ModelForm):
    #TODO: pwd with miniscule, maj, lettres et chiffres
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['password'].required = False
        self.fields['password2'].required = False


    def clean(self):
        super(UserForm, self).clean()
        data = self.cleaned_data
        if data["password"] != data["password2"]:
            raise forms.ValidationError({'password': ["Passwords must be the same."]})
        elif len(data["password"]) <6:
            raise forms.ValidationError({'password': ["password must be at least 6 characters"]})
        return data


    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
        'placeholder': 'Confirm your password'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
        'placeholder': 'Your password'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your username'}), 
        max_length=30,
        required=True )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Your email'}),
        required=True,
        label= 'Your Email',

        max_length=75 )

    class Meta:
        model = User
        fields = ['username', 'email', 'password','password2']



class ProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':
        'Like #movies #kittens #travel #teacher #newyork'}), 
        max_length=300)
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':
        'World'}), required=False)
    bd = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':
        'University'}), required=False)
    job = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':
        'Like #developer #administrator'}), required=False)
    class Meta:
        model = Profile
        fields = ('bio','location','avatar','cover','bd','job')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('textc',)