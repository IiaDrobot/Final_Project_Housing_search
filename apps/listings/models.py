from django.db import models
from django.conf import settings
from django.db.models import Avg

ROOM_CHOICES = [(i, str(i)) for i in range(1, 11)]

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    rooms = models.IntegerField(choices=ROOM_CHOICES)

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

    average_rating = models.FloatField(default=0.0)

    view_count = models.PositiveIntegerField(default=0)


    def increment_view_count(self):
        self.view_count = models.F('view_count') + 1
        self.save(update_fields=['view_count'])

    def update_average_rating(self):
        from apps.reviews.models import Review  # избегаем циклического импорта
        avg = Review.objects.filter(listing=self).aggregate(avg=Avg('rating'))['avg'] or 0.0
        self.average_rating = round(avg, 1)
        self.save()

    def __str__(self):
        owner = self.owner.username if self.owner else "No Owner"
        return f"{self.title} - {self.city} ({owner})"

    class Meta:
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["city"]),
        ]
class ListingViewHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f'{self.user} viewed {self.listing} at {self.viewed_at}'