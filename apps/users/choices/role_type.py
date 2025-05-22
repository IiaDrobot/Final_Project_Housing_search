from enum import Enum

class RoleType(str, Enum):
    ADMIN = "Администратор"
    MODERATOR = "Модератор"
    TENANT = "Арендатор"
    LESSOR = "Арендодатель"

    @classmethod
    def choices(cls):
        return [(member.name, member.value) for member in cls]
