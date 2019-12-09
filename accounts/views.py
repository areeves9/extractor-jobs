from django.urls import reverse_lazy

from accounts.models import SiteUser

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from accounts.forms import UserRegisterForm

# Create your views here.


class RegistrationView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/registration_form.html'


class UserProfileView(DetailView):
    """
    Get extended SiteUser information for
    request.user. Should direct to the template
    for this view upon login.
    """
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class UserDetailView(DetailView):
    '''
    Get detail of employee for profile. Return the
    request.user object for the current logged in
    user.
    '''
    model = SiteUser
    context_object_name = 'user'


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


class UserListView(ListView):
    """
    List of SiteUser objects, with fk back to batch.
    """
    model = SiteUser
    context_object_name = 'users'
