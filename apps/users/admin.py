from django.contrib import admin
from apps.users.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from apps.users.choices.role_type import RoleType
from django.contrib.auth.models import Group

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('username','email','role','is_staff','is_active')
    list_filter = ('is_staff','is_active','role')
    search_fields = ('username','email','first_name','last_name','role')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username','email', 'password',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name','phone','role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )

    admin.site.unregister(Group)
    admin.site.register(Group)