from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from accounts.forms import UserRegisterForm

# Create your views here.


class RegistrationView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/registration_form.html'
