from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager,AbstractBaseUser,Group,Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.users.choices.role_type import RoleType  # Импорт Enum с ролями


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(_('email address'), max_length=50, unique=True)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    role = models.CharField(
        max_length=30,
        choices=RoleType.choices(),
        default=RoleType.TENANT.name
    )
    phone = models.CharField(max_length=50, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(Group,
    related_name='custom_user_groups',blank=True)
    user_permissions = models.ManyToManyField(Permission,
    related_name='custom_user_permissions',blank=True)


    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "role"]

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"



def get_first_admin() -> User:
    return User.objects.filter(role="ADMIN").first().id



