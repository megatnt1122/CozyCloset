from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def your_closet(request):
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/your_closet.html', context)

@login_required
def add_closet(request):
    ##u_form = UserUpdateForm(instance=request.user)
    cu_from = ClosetForm(instance=request.user)
    ci_from = ClosetUpdateForm(instance=request.user.profile)

    if request.method == 'POST':
        cu_form = ClosetForm(request.POST, instance=request.user)
        ci_form = ClosetUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            cu_form.save()
            ci_form.save()
            messages.success(request, f'Your closet has been updated!')
            return redirect('your_closet') ##"your_closet"

    else:
        cu_form = ClosetForm(instance=request.user)
        ci_form = ClosetUpdateForm(instance=request.user.profile)
    
    context = {
        'cu_form': cu_form,
        'ci_form': ci_form
    }

    return render(request, 'users/add_closet.html', context)
