from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .models import CustomUser, Skill
# from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm, Addskill
# from django.contrib.auth import get_user_model
from .utils import developer_search, paginate

def user_detail(request, pk):
    '''
    returns setails of user with id=pk
    '''
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
    '''
    logs a registered user in
    '''
    page = 'login'
    # if a logged in user tries to access this view with the bare url
    if request.user.is_authenticated:
        return redirect('users:user_list')

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
            return redirect('users:user_list')
        else:
            context = {
                'next': next,
                'email': email,
                'page': page
            }
            messages.error(request, "Password/Username is incorrect")
            return render(request, 'users/login_form.html', context)

    return render(request, 'users/login_form.html', {'next':next, 'page': page})

def UserLogout(request):
    '''
    logout a logged in user
    '''
    logout(request)
    messages.info(request, "You've been logged out")
    return redirect('users:login')




@login_required
def UserList(request):
    '''
    return a list of all users
    '''
    context = developer_search(request)
    query_set, _range = paginate(request, 6, context["users"])
    context["users"] = query_set
    context["range"] = _range

    return render(request, 'users/user_list.html', context)

def register(request):
    '''
    register and then login a new user
    '''
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
    '''
    show the accounts page for the logged in user
    '''
    user = request.user
    skills = user.skill_set.all()

    context = {
        'user': user,
        'skills': skills
    }
    return render(request, 'users/account.html', context)

@login_required
def editAccount(request):
    '''
    edit user information
    '''
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user = form.save()
            return redirect('users:account')
        else:
            return render(request, 'users/user_form.html', {'form': form})
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'users/user_form.html', context)

@login_required
def addskill(request):
    '''
    add skills
    '''
    if request.method == "POST":
        form = Addskill(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user
            skill.save()
            return redirect("users:account")
        else:
            return render(request, "users/skill_form.html", {"form": form})
    else:
        form = Addskill()
        context = {
            "form": form
        }
        return render(request, "users/skill_form.html", context)


@login_required
def updateskill(request, pk):
    '''
    update skills
    '''
    user = request.user

    if not user.skill_set.filter(id=pk).exists():
        return redirect(reverse("users:account"))

    skill = Skill.objects.get(id=pk)

    if request.method == "POST":
        form = Addskill(request.POST, instance=skill)

        if form.is_valid():
            form.save()
            return redirect(reverse("users:account"))
        else:
            return render(request, "users/skill_form.html", {"form": form})

    form = Addskill(instance=skill)
    return render(request, "users/skill_form.html", {"form": form})

@login_required
def delete_skill(request, pk):
    '''
    delete skills
    '''
    user = request.user

    if user.skill_set.filter(id=pk).exists():
        skill = user.skill_set.get(id=pk)
        next = request.GET.get('next', '')
        context = {'object': skill, 'next': next}
    else:
        return redirect("users:account")

    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Delete Sucessful")
        return redirect("users:account")
    return render(request, 'confirm_delete.html', context)
