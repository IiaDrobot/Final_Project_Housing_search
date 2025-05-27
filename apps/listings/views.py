from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from .models import Listing
from .serializers import ListingSerializer,ListingViewHistorySerializer
from .filters import ListingFilter
from .models import Listing, ListingViewHistory
from django.utils import timezone



class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ListingFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['GET'])
def view_listing(request, pk):
    try:
        listing = Listing.objects.get(pk=pk)
        listing.view_count = F('view_count') + 1
        listing.save(update_fields=['view_count'])
        listing.refresh_from_db()


        if request.user.is_authenticated:
            ListingViewHistory.objects.update_or_create(
                user=request.user,
                listing=listing,
                defaults={'viewed_at': timezone.now()}
            )

        serializer = ListingSerializer(listing)
        return Response(serializer.data)
    except Listing.DoesNotExist:
        return Response({'error': 'Listing not found'}, status=status.HTTP_404_NOT_FOUND)


class ListingViewHistoryListView(generics.ListAPIView):
        serializer_class = ListingViewHistorySerializer
        permission_classes = [permissions.IsAuthenticated]

        def get_queryset(self):
            return ListingViewHistory.objects.filter(user=self.request.user).order_by('-viewed_at')

