from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from accounts.forms import UserAdminCreationForm, UserAdminChangeForm
from accounts.models import SiteUser, CandidateProfile


class SiteUserAdmin(BaseUserAdmin):
    #  Includes forms to add and change User instances
    forms = UserAdminChangeForm
    add_form = UserAdminCreationForm

    #  Fields to be shown in displaying the user model.
    #  The following overrides fields in base UserAdmin
    #  that point to specific fields of auth.User.
    list_display = (
        'email',
        'account_type',
        'display_name',
        'first_name',
        'last_name',
        'date_joined',
        'location_state',
        'is_admin',
        'is_active',
    )
    list_filter = (
        ('location_state'),
        ('account_type'),
        ('is_active'),
    )
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('User Information', {'fields': (
            'is_active',
            'first_name',
            'last_name',
            'image',
            'bio',
            'location_state',
            'location_city',
            'phone_number',
            'account_type',)}),
        ('Permissions', {'fields': (
            'is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # These are the form fields when Add User button is clicked in admin.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'display_name',
                'account_type',
                'password1',
                'password2',
            ),
        }),
    )
    search_fields = ('email', 'display_name')
    ordering = ('email',)
    filter_horizontal = ()


class CandidateProfileModelAdmin(admin.ModelAdmin):
    list_display = ("user", "education", "speciality", "field_of_study", "headline", "title")
    list_display_link = ("user",)

    class Meta:
        model = CandidateProfile


admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(CandidateProfile, CandidateProfileModelAdmin)