
from rest_framework import serializers
from .models import Review
from apps.booking.models import Booking
from django.utils import timezone

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'listing', 'rating', 'comment', 'created_at']
        read_only_fields = ['reviewer', 'created_at']

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        review = super().create(validated_data)

        review.listing.update_average_rating()

        return review

    def validate(self, data):
        user = self.context['request'].user
        listing = data['listing']

        has_booking = Booking.objects.filter(
            tenant=user,
            listing=listing,
            status='confirmed',
           #end_date__lt=timezone.now()
        ).exists()

        if not has_booking:
            raise serializers.ValidationError("Вы можете оставить отзыв только после завершенного бронирования.")
        return data