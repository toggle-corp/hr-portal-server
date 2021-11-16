from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.user.models import User, UserDepartment, Department
# Register your models here.


class DepartmentInline(admin.TabularInline):
    model = UserDepartment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [
        DepartmentInline,
    ]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email',
                'primary_email', 'secondary_email', 'address', 'primary_phone_number',
                'secondary_phone_number', 'avatar', 'avatar_url',
                'joined_at', 'birthday', 'gender'
            )
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    list_display = (
        'full_name', 'email', 'is_superuser', 'joined_at', 'birthday', 'gender',
    )
    list_filter = (
        'gender', 'is_staff', 'is_superuser', 'is_active'
    )


admin.site.register(UserDepartment)
admin.site.register(Department)
