from enum import Enum

from django.conf.global_settings import ADMINS


class RoleType(str, Enum):
    ADMIN = "Администратор"
    MODERATOR = "Модератор"
    TENANT = "Арендатор"
    LESSOR = "Арендодатель"

    @classmethod
    def choices(cls):
        return [(member.name, member.value) for member in cls]
