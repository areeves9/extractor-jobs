from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from accounts.forms import UserAdminCreationForm, UserAdminChangeForm
from accounts.models import SiteUser


class SiteUserAdmin(BaseUserAdmin):
    #  Includes forms to add and change User instances
    forms = UserAdminChangeForm
    add_form = UserAdminCreationForm

    #  Fields to be shown in displaying the user model.
    #  The following overrides fields in base UserAdmin
    #  that point to specific fields of auth.User.
    list_display = (
        'email',
        'display_name',
        'first_name',
        'last_name',
    )
    list_filter = (
        ('display_name'),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('User Information', {'fields': (
            'first_name',
            'last_name',
            'display_name',
            'phone_number',)}),
        ('Permissions', {'fields': (
            'is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'display_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'display_name')
    ordering = ('email',)
    filter_horizontal = ()
# Register your models here.
# comment


admin.site.register(SiteUser, SiteUserAdmin)