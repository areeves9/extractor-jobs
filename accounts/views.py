from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from accounts.models import SiteUser
from accounts.forms import CandidateProfileForm, UserRegisterForm, SiteUserForm

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required


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
    queryset = SiteUser.objects.filter(is_active=True, account_type='CANDIDATE')
    context_object_name = 'users'


@login_required
def candidate_profile_update(request):
    print(request.user)
    user_form = SiteUserForm(request.POST or None, instance=request.user)
    candidate_profile_form = CandidateProfileForm(request.POST or None, instance=request.user.candidateprofile)
    if user_form.is_valid() and candidate_profile_form.is_valid():
        user = user_form.save(commit=False)
        profile = candidate_profile_form.save(commit=False)
        user.save()
        profile.save()
        return redirect("accounts:profile")
    else:
        user_form = SiteUserForm(instance=request.user)
        candidate_profile_form = CandidateProfileForm(instance=request.user.candidateprofile)
    context = {
        "user_form": user_form,
        "candidate_profile_form": candidate_profile_form,
    }
    return render(request, "accounts/candidate_profile_update.html", context)