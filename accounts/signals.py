from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib import messages


def on_login(sender, user, request, **kwargs):
    messages.success(request, '{} logged in successfully.'.format(user.display_name))


def on_logout(sender, user, request, **kwargs):
    messages.success(request, '{} logged in successfully.'.format(user.display_name))


user_logged_in.connect(on_login)
user_logged_out.connect(on_logout)