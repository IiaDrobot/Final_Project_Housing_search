from rest_framework import serializers
from .models import Listing, ListingViewHistory


class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Listing
        fields = '__all__'

class ListingViewHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingViewHistory
        fields = ['listing', 'viewed_at']
