<<<<<<< HEAD
from django.views.generic import CreateView
from django.core.mail import send_mail

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "users/signup.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        send_mail_ls(email)
        return super().form_valid(form)


def send_mail_ls(email):
    send_mail('Подтверждение регистрации Yatube', 'Вы зарегистрированы!',
              'admin@yatube.ru', [email], fail_silently=False)
=======
from django.views.generic import CreateView
from django.core.mail import send_mail

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "users/signup.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        send_mail_ls(email)
        return super().form_valid(form)


def send_mail_ls(email):
    send_mail('Подтверждение регистрации Yatube', 'Вы зарегистрированы!',
              'admin@yatube.ru', [email], fail_silently=False)
>>>>>>> e00ceddaa1758d008aea9fd3ff70b76728ca2368
