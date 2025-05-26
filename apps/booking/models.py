from django.db import models
from django.conf import settings
from apps.listings.models import Listing # Импортируем модель объявления


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'В ожидании'
        CONFIRMED = 'confirmed', 'Подтверждено'
        CANCELLED = 'cancelled', 'Отменено арендатором'
        DECLINED = 'declined', 'Отклонено арендодателем'
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} — {self.tenant.username} ({self.start_date} → {self.end_date})"
