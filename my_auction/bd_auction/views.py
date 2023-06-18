from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from .form import RegisterForm, InfoForm
from .models import InfoUser


class Register(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = 'http://127.0.0.1:8000/admin/'

    def form_valid(self, form):
        form.instance.is_staff = '1'
        user = form.save()
        login(self.request, user)
        return redirect('http://127.0.0.1:8000/admin/')


def f (request):
    print(request.user)
    if request.method == 'POST':
        print(request.POST)
        user_form = RegisterForm(request.POST, instance=request.user)
        profile_form = InfoForm(request.POST, instance=request.user.infouser)
        print(profile_form)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('http://127.0.0.1:8000/admin/')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = RegisterForm(instance=request.user)
        profile_form = InfoForm(instance=request.user.infouser)
    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def update_profile(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST, request)
        if user_form.is_valid():
            user_form.save()
        else:
            messages.error(request, ('Please correct the error below.'))
        id_user = User.objects.get(username=str(request.POST['username']))
        print(id_user.id)
        info_ = InfoUser(
            user_id=id_user,
            username_tg=request.POST['username_tg']
        )
        info_.save()
        return redirect('http://127.0.0.1:8000/admin/')
    else:
        user_form = RegisterForm()
        profile_form = InfoForm()
        return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form})