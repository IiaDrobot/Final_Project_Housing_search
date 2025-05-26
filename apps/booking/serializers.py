from rest_framework import serializers
from .models import Booking
from datetime import timedelta
from django.utils import timezone

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['tenant', 'status', 'created_at']

    def validate(self, data):
        listing = data['listing']
        start = data['start_date']
        end = data['end_date']

        if start >= end:
            raise serializers.ValidationError("Дата начала должна быть раньше даты окончания.")

        overlapping = Booking.objects.filter(
            listing=listing,
            start_date__lt=end,
            end_date__gt=start
        ).exists()

        if overlapping:
            raise serializers.ValidationError("Жильё уже забронировано на указанные даты.")

        today = timezone.now().date()
        if (start - today).days < 2:
            raise serializers.ValidationError("Бронирование возможно минимум за 2 дня до заезда.")

        return data


    def create(self, validated_data):
        validated_data['tenant'] = self.context['request'].user
        return super().create(validated_data)



