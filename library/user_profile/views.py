from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserUpdateForm, UserProfileUpdateForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User


@login_required
def view_my_profile(request):
    return render(request, 'user_profile/view_profile.html')

def view_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_profile/view_profile.html')

@login_required
def edit_profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'vartotojo: { request.user } duomeny atnaujinti')
            return redirect('view_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.user_profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user_profile/edit_profile.html', context)


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        error = False
        if password and password != password2:
            messages.error(request, 'Slaptazodis nesutampa arba neivesti')
            error = True
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Vartotojas {username} jau egzsituoja')
            error = True
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Vartotojas su el. pastu {email} jau egzsituoja arba neivestas.')
            error=True
        if error:
            return redirect('register')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f'Vartotojas {username} uzregistruotas sekmingai')
            return redirect('index')
    return render(request, 'user_profile/register.html')