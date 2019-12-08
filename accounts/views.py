from django.urls import reverse_lazy

from accounts.models import SiteUser

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from accounts.forms import UserRegisterForm

# Create your views here.


class RegistrationView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/registration_form.html'


class UserDetailView(DetailView):
    '''
    Get detail of employee for profile. Return the
    request.user object for the current logged in
    user.
    '''
    def get_object(self):
        return self.request.user


class UserUpdateView(UpdateView):
    """
    Updates Employee instance.
    """
    model = SiteUser
    fields = (
        'first_name',
        'last_name',
        'display_name',
        'bio',
        'location_city',
        'location_state',
        'image',
        'phone_number',

    )
    success_url = reverse_lazy('accounts:profile')
