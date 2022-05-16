from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import NotificationChannel, UserDevices

User = get_user_model()

# class UserAdmin(admin.ModelAdmin):
#     search_fields = ['email']
#     class Meta:
#         model = User


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'admin']
    list_filter = ('admin', 'is_active', 'staff')
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'password1', 'password2', 'admin', 'staff', 'is_active', 'normal_user', 'advanced_user', )}
        ),
    )
    search_fields = ('email', 'full_name',)
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin,)
admin.site.register(UserDevices,)
admin.site.register(NotificationChannel)

