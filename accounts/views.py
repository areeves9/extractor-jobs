from django.urls import reverse_lazy

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from accounts.models import SiteUser, Experience
from accounts.forms import UserRegisterForm, UserUpdateForm, ExperienceForm

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
    form_class = UserUpdateForm
    success_url = reverse_lazy('accounts:profile')


class UserListView(ListView):
    """
    List of SiteUser objects, with fk back to batch.
    """
    queryset = SiteUser.objects.filter(is_active=True, is_business=False)
    context_object_name = 'users'


class ExperienceView(CreateView):
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ExperienceView, self).form_valid(form)

    model = Experience
    form_class = ExperienceForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/experience_form.html'


class ExperienceUpdateView(UpdateView):
    """
    Updates Experience instance.
    """
    model = Experience
    form_class = ExperienceForm
