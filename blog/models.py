from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse 
from django.contrib.auth.models import Permission, User
from tinymce.models import HTMLField
from tinymce import models as tinymce_models 
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(blank=True)
    cover = models.FileField(blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.TextField(max_length=200, blank=True)
    bd = models.FileField(blank=True, null=True) 
    job = models.FileField(blank=True)

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        return self.model.objects(user=user.id)

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()

post_save.connect(create_user_profile, sender=User)


class Post(models.Model):
    user = models.ForeignKey(User, null=True)
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=1000, blank=True)
    #slug = models.SlugField(max_length=255, null=True, blank=True) 
    text = tinymce_models.HTMLField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.user
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    #after creating new post redirect to detail page with a primary key 'self.pk'    
    def get_absolute_url (self):
        return reverse('blog:index')
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', null=True,related_name='comments')
    user = models.ForeignKey(User, max_length=200, blank=True, null=True)
    textc = models.CharField(null=True,max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.textc