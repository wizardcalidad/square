from django.contrib import admin
from .models import Profile, Post

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','bio','email', 'date_of_birth', 'photo']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','content','date_posted','author']