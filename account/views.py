from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegisterForm, UserUpdateForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from .models import Post


# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'account/home.html', context)


def about(request):
    return render(request, 'account/about.html')


@login_required
def dashboard(request):
    return render(request,
                  'account/profile.html',
                  {'section': 'dashboard'})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password= cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated ', 'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Disabled account')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])

            new_user.save()
            Profile.objects.create(user=new_user)

            return render(request,
                        'account/register_done.html',
                        {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,
                                instance=request.user.profile)
        p_form = ProfileEditForm(request.POST,
                                 request.FILES,
                                 instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile updated successfully')
            return redirect('profile')


    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'account/profile.html', context)


def edit(request):
     return render(request,
                  'account/edit.html',
                  {'user_form': u_form})
