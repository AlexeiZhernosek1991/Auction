from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from .form import RegisterForm, InfoForm
from .models import InfoUser, Reg_tg


def update_profile(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST, request)
        if user_form.is_valid():
            user_form.save()
        else:
            messages.error(request, ('Please correct the error below.'))
        id_user = User.objects.get(username=str(request.POST['username']))
        try:
            tg_id = Reg_tg.objects.get(username=str(request.POST['username_tg']))
            tg_id = tg_id.id_tg
        except:
            tg_id = '@введен не верно'
        info_ = InfoUser(
            user_id=id_user,
            username_tg=request.POST['username_tg'],
            tg_id=tg_id
        )
        info_.save()
        return redirect('http://127.0.0.1:8000/admin/')
    else:
        user_form = RegisterForm()
        profile_form = InfoForm()
        return render(request, 'register.html', {
            'user_form': user_form,
            'profile_form': profile_form})
