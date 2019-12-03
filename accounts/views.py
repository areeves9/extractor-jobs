from django.urls import reverse, reverse_lazy
from accounts.models import SiteUser
from django.views.generic.edit import CreateView
from accounts.forms import UserRegisterForm, RegisterForm

# Create your views here.


class RegistrationView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/registration_form.html'
