from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
from django.utils import timezone


class Profile(models.Model):
    first_name = models.CharField(max_length=200, default='firstname')
    last_name = models.CharField(max_length=200, default='lastname')
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(default="A brief bio about you...", max_length=200)
    email = models.EmailField()
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=200, blank=True)
    photo = models.ImageField( default='default.jpg', upload_to='users/%Y/%m/%d/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, default='uuid-uid')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}-{self.created}'


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title