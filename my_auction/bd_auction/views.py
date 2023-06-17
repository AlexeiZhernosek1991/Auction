from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views.generic import CreateView



class Register(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = 'http://127.0.0.1:8000/admin/'

    def form_valid(self, form):
        form.instance.is_staff = '1'
        user = form.save()
        login(self.request, user)
        return redirect('http://127.0.0.1:8000/admin/')



