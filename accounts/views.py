from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin


from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from accounts.models import SiteUser, Experience, Skill
from accounts.forms import UserRegisterForm, UserUpdateForm, ExperienceForm, SkillForm

# Create your views here.


class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/registration_form.html'
    success_message = 'User sucessfuly registered.'

    def form_valid(self, form):
        # bound form instance has the user data
        # save it to add user to db
        form.save()
        # authenticate user then login
        user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'],)
        login(self.request, user)
        return HttpResponseRedirect(reverse('jobs:job_list'))


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
    paginate_by = 10


class MyJobsView(ListView):
    """
    Show all job posts liked by the user with pagination.
    """
    template_name = 'accounts/my_jobs.html'
    context_object_name = 'my_jobs'
    paginate_by = 10

    def get_queryset(self):
        return SiteUser.objects.filter(email=self.request.user).first().jobs_liked.all()


class UserUpdateView(SuccessMessageMixin, UpdateView):
    """
    Updates Employee instance.
    """
    model = SiteUser
    form_class = UserUpdateForm
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Account sucessfuly updated.'


class UserListView(ListView):
    """
    List of SiteUser objects, with fk back to batch.
    """
    queryset = SiteUser.objects.filter(is_active=True, is_business=False)
    context_object_name = 'users'


class ExperienceView(CreateView):
    """
    Create an Expereince instance.
    """
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ExperienceView, self).form_valid(form)

    model = Experience
    form_class = ExperienceForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/experience_form.html'


class ExperienceDetailView(DetailView):
    '''
    Get detail of employee for profile. Return the
    request.user object for the current logged in
    user.
    '''
    model = Experience
    context_object_name = 'experience'


class ExperienceUpdateView(UpdateView):
    """
    Updates Experience instance.
    """
    model = Experience
    form_class = ExperienceForm
    success_url = reverse_lazy('accounts:profile')


class SkillDetailView(DetailView):
    '''
    Get detail of employee for profile. Return the
    request.user object for the current logged in
    user.
    '''
    model = Skill
    context_object_name = 'skill'


class SkillUpdateView(UpdateView):
    """
    Update skill instance - add or remove tags.
    """
    model = Skill
    form_class = SkillForm
    success_url = reverse_lazy('accounts:profile')
