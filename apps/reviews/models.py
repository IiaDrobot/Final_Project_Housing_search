
from django.db import models
from django.conf import settings

class Review(models.Model):
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_left')
    listing = models.ForeignKey(
        'listings.Listing', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'listing')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer.email} - {self.listing.title} ({self.rating})"
