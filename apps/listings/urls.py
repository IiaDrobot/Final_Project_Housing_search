from django.urls import path
from .views import ListingListCreateView, ListingRetrieveUpdateDestroyView

urlpatterns = [
    path('listings/', ListingListCreateView.as_view(), name='listing-list-create'),
    path('listings/<int:pk>/', ListingRetrieveUpdateDestroyView.as_view(), name='listing-detail'),
]
