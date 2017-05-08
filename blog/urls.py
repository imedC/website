from django.conf.urls import url
from . import views
from django.conf import settings
from blog.views import DetailView, UpdateView, DeleteView, IndexView
app_name = 'blog' #ceci est pour indiquer que tt les noms des url ( details, comment..) appartiennent à l'app blog

urlpatterns = [
    # this section contains the different url in /blog/
    # /blog/
    url(r'^$',views.IndexView, name = 'index'),
    url(r'^register/$', views.UserFormView.as_view(), name = 'register'),
    url(r'^login/$',  views.login_user, name = 'login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    
    url(r'^(?P<username>\w+)/$',  views.Profil, name = 'profil'),
    url(r'^(?P<username>\w+)/edit/$', views.update_profile, name='edit_profile'),
    #/blog/post_id/
    url(r'^detail/(?P<pk>\d+)/$', views.DetailView, name = 'detail'),

    url(r'^post/add/$', views.post_new, name = 'creat' ),
   
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^post/(?P<pk>\d+)/$', views.post_edit , name = 'update'),
    url(r'^comment/(?P<pk>\w+)/remove/$', views.CommentDeleteView.as_view(), name='comment_remove'),
    url(r'^post/(?P<pk>\w+)/delete/$', DeleteView.as_view(), name = 'delete'),

    
    ]