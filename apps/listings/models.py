from django.db import models
from django.conf import settings


ROOM_CHOICES = [(i,str(i)) for i in range(1,11)]

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    rooms = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])

    HOUSE_TYPES = [
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('studio', 'Студия'),
        ('room', 'Комната'),
    ]
    property_type = models.CharField(max_length=20, choices=HOUSE_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings'
    )

    def __str__(self):
        return f"{self.title} - {self.city} ({self.owner.username})"

    class Meta:
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["city"]),
        ]


    # Владелец (арендодатель)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings'
    )

    def __str__(self):
        return f"{self.title} - {self.city}"
