import datetime

from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

# from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

# from django.views.generic.list import View
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    FormView,
    DeleteView
)
from django.views.generic.list import ListView

from accounts.tokens import account_activation_token
from accounts.models import SiteUser, Experience, Skill
from accounts.forms import (
    UserRegisterForm,
    UserUpdateForm,
    ExperienceForm,
    SkillForm,
    BusinessRequestForm,
    )

# Create your views here.


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = SiteUser.objects.get(pk=uid)
            print(user)
        except(TypeError, ValueError, OverflowError, SiteUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(user.get_absolute_url())
        else:
            return render(request, 'registration/activation_invalid.html')


class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('accounts:register_complete')
    template_name = 'registration/registration_form.html'
    success_message = 'Please check your email for confirmation.'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            to_email = form.cleaned_data['email']
            form.save()

            subject = 'Activate your account.'
            current_site = get_current_site(request)
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(form.instance.pk)),
                'token': account_activation_token.make_token(form.instance)
            })
            email = EmailMessage(subject, message, to=[to_email, ])
            email.send()
            return redirect(self.success_url)
        else:
            form = self.form_class()
            return form


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
        return SiteUser.objects.filter(
            email=self.request.user
        ).first().jobs_liked.all()


class UserUpdateView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    """
    Updates Employee instance.
    """
    model = SiteUser
    form_class = UserUpdateForm
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Account sucessfuly updated.'

    def test_func(self):
        return self.request.user.pk == self.get_object().pk


class UserListView(ListView):
    """
    List of SiteUser objects, with fk back to batch.
    """
    queryset = SiteUser.objects.filter(is_active=True, is_business=False)
    context_object_name = 'users'
    paginate_by = 10


class ExperienceView(SuccessMessageMixin, CreateView):
    """
    Create an Expereince instance.
    """
    model = Experience
    form_class = ExperienceForm
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Job experience sucessfully added.'
    template_name = 'accounts/experience_form.html'

    def form_valid(self, form):
        if form.instance.is_present_employeer:
            form.instance.end_month = datetime.datetime.now().month
            form.instance.end_year = datetime.datetime.now().year
        form.instance.user = self.request.user
        return super(ExperienceView, self).form_valid(form)


class ExperienceDetailView(DetailView):
    '''
    Get detail of employee for profile. Return the
    request.user object for the current logged in
    user.
    '''
    model = Experience
    context_object_name = 'experience'


class ExperienceUpdateView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    """
    Updates Experience instance.
    """
    model = Experience
    form_class = ExperienceForm
    success_message = 'Job experience successfully updated.'
    success_url = reverse_lazy('accounts:profile')

    def test_func(self):
        return self.request.user.experience_set.filter(pk=self.get_object().pk).exists()


class ExperienceDeleteView(DeleteView):
    """
    Delete an experience instance from user profile.
    """
    model = Experience
    success_url = reverse_lazy('accounts:profile')



class SkillDetailView(DetailView):
    '''
    Get detail of employee for profile. Return the
    request.user object for the current logged in
    user.
    '''
    model = Skill
    context_object_name = 'skill'


class SkillUpdateView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    """
    Update skill instance - add or remove tags.
    """
    model = Skill
    form_class = SkillForm
    success_message = 'Skills successfully updated.'
    success_url = reverse_lazy('accounts:profile')

    def test_func(self):
        return self.request.user.skill.pk == self.get_object().pk


class BusinessRequestView(SuccessMessageMixin, FormView):
    """
    Submit an email to site admin for business account.s
    """
    template_name = 'accounts/business_request_form.html'
    form_class = BusinessRequestForm
    success_url = '/jobs/'
    success_message = 'Request successfully sent.'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            subject = 'Request for business account from {}'.format(request.user)
            from_mail = request.user.email
            email_recipient = 'areeves9@icloud.com'
            text_content = 'Request for business account from {}.'.format(request.user)
            html_message = render_to_string('accounts/business_request_email.html', {
                'user': request.user,
                'business_name': form.cleaned_data['business_name'],
                'location': form.cleaned_data['location'],
                'address': form.cleaned_data['address'],
                'license_id': form.cleaned_data['license_id'],

            })
            msg = EmailMultiAlternatives(
                subject, text_content, from_mail, [email_recipient, ]
            )
            msg.attach_alternative(html_message, "text/html")
            msg.mixed_subtype = 'related'
            msg.send()

        return super().form_valid(form)
