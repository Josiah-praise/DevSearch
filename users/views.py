from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm
from django.contrib.auth import get_user_model


        
def users(request, pk):
    user = CustomUser.objects.get(id=pk)
    has_description= user.skill_set.exclude(description__exact='')
    no_description = user.skill_set.filter(description='')
    context = {
        'user': user,
        'has_desc': has_description,
        'no_desc': no_description,
    }
    return render(request, 'users/customuser_detail.html', context)


def UserLogin(request):
    
    page = 'login'
    # if a logged in user tries to access this view with the bare url
    if request.user.is_authenticated:
        return redirect(reverse('users:user_list'))
    next = request.GET.get('next', None)

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        next = request.GET.get('next', None)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user.get_full_name()}')
            if next is not None:
                return redirect(next)
            return redirect(reverse('users:user_list'))
        else:
            context = {
                'next': next,
                'email': email,
                #'password': password it's prolly not safe to send password to the raw template
                'page': page
            }
            messages.error(request, "Password/Username is incorrect")
            return render(request, 'users/login_form.html', context)

    return render(request, 'users/login_form.html', {'next':next, 'page': page})

def UserLogout(request):
    logout(request)
    messages.info(request, "You've been logged out")
    return redirect(reverse('users:login'))

class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'users/user_list.html'


def register(request):
    
    if request.user.is_authenticated:
        return redirect(reverse('users:user_detail', args=(request.user.id,)))

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account Created")
            return redirect('users:edit_account')
        else:
            for field, errors in form.errors.items():
                print(f"Field '{field}': {', '.join(errors)}")
            messages.error(request, "SignUp Error")
            return render(request, 'users/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def userAccount(request):
    user = request.user
    skills = user.skill_set.all()
    
    context = {
        'user': user,
        'skills': skills
    }
    messages.info(request, f"Welcome {user.get_full_name()}")
    return render(request, 'users/account.html', context)

@login_required
def editAccount(request):

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            user = form.save()
            return redirect(reverse('users:account'))
        else:
            return render(request, 'users/user_form.html', {'form': form})
    else:
        form = UserUpdateForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'users/user_form.html', context)