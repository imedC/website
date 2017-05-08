from .models import Post, Comment
from django.views import generic
from django.views.generic import View, ListView, UpdateView, DeleteView 
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, Http404 
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect 
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, PostForm, ProfileForm, CommentForm  
from django.contrib import messages 
from django.utils import timezone 
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView


def Profil(request, username):
	if request.user.is_authenticated():
		base_template_name = 'blog/base.html'
	else:
		base_template_name = 'blog/visitor.html'

	user = User.objects.get(username= username)

	logged_in_user_posts = Post.objects.filter(user=user)
	context = {'base_template_name':base_template_name}
	return render(request, 'blog/profil.html',
	{'user':user, 'posts':logged_in_user_posts,'base_template_name':base_template_name })


		
def update_profile(request, username):
	if request.method == 'POST':
		profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
		if profile_form.is_valid():
			profile_form.save()
			messages.success(request, ('Your profile was successfully updated!'))
			return redirect('blog:index')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		profile_form = ProfileForm(instance=request.user.profile)
	return render(request, 'blog/edit_profile.html', {
		'profile_form': profile_form })


def IndexView(request):
	if request.user.is_authenticated():
		base_template_name = 'blog/base.html'
	else:
		base_template_name = 'blog/visitor.html'
	posts = Post.objects.all().order_by('-published_date')
	return render(request, 'blog/index.html', {'posts':posts,'base_template_name':base_template_name})

def add_comment_to_post(request, pk):
	if request.user.is_authenticated():
		base_template_name = 'blog/base.html'
	else:
		base_template_name = 'blog/visitor.html'
	post = get_object_or_404(Post, pk=pk)
	form = CommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.user = request.user
		comment.post = post
		comment.save()
		return redirect('blog:index')
	return render(request, 'blog/index.html', {'post':post,'form': form,
	'base_template_name':base_template_name})


def DetailView(request, pk):
	if request.user.is_authenticated():
		base_template_name = 'blog/base.html'
	else:
		base_template_name = 'blog/visitor.html'
	post = get_object_or_404(Post, pk=pk)
	form = CommentForm(request.POST or None)
	if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('blog:detail', pk=pk)
	return render(request,'blog/detail.html',{'post':post,'form':form,
	'base_template_name':base_template_name})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.published_date = timezone.now()
			post.save()
			return HttpResponseRedirect(post.get_absolute_url())
	else:
		form = PostForm()
	return render(request, 'blog/post_form.html', {'form': form})
	
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.published_date = timezone.now()
			post.save()
			return HttpResponseRedirect(post.get_absolute_url())
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_form.html', {'form': form}) 
	

class DeleteView(generic.DeleteView):
	model = Post
	success_url = reverse_lazy('blog:index')


def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('blog:index', pk=comment.post.pk)


class CommentDeleteView(generic.DeleteView):
	model = Comment
	success_url = reverse_lazy('blog:index')


class UserFormView(View):
	form_class = UserForm
	template_name = 'blog/registration.html'

	#Display blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	#process from data
	
	def post(self, request):
		form = self.form_class(request.POST)
	
		if form.is_valid():

			user = form.save(commit=False)

			#cleaned data

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			# returns user objects if credentials are correct
			user = authenticate(username=username, password= password)
			messages.add_message(request, messages.SUCCESS, 'Your account were successfully created.')
			
			if user is not None:

				if user.is_active:
					login(request, user)
					posts = Post.objects.all()
					base_template_name = 'blog/base.html'
					model = Post
					return render(request, 'blog/index.html',{'posts':posts,'base_template_name':base_template_name}) 
		return render (request, self.template_name, {'form': form})



def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				base_template_name = 'blog/base.html'
				posts = Post.objects.all()
				return render(request, 'blog/index.html', {'posts':posts,'base_template_name':base_template_name})
			else:
				return render(request, 'blog/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'blog/login.html', {'error_message': 'Invalid login'})
	return render(request, 'blog/login.html')

def logout_user(request):
	logout(request)
	form = UserForm(request.POST or None)
	context = {
		"form": form,
	}
	return render(request, 'blog/login.html', context)

#render: conbine un gabarit donné avec un dictionnaire contexte donné
#et renvoie un objet HttpResponse avec le texte résultant. 
#redirect: Renvoie une réponse HttpResponseRedirect à l’URL soit en lui passant
 #un objet ( getabsoluteurl) ou en lui passant un vue ( reverse)
























