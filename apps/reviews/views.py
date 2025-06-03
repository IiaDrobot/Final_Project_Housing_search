
from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        listing_id = self.request.query_params.get('listing_id')
        if listing_id:
            return self.queryset.filter(listing_id=listing_id)
        return self.queryset

    def perform_create(self, serializer):
        user = self.request.user
        listing = serializer.validated_data.get('listing')
       # serializer.save()
