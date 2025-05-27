from django.urls import path
from .views import (
    ListingListCreateView,
    ListingRetrieveUpdateDestroyView,
    view_listing,

)
from apps.listings.views import  ListingViewHistoryListView

urlpatterns = [
    path('listings/', ListingListCreateView.as_view(), name='listing-list-create'),
    path('listings/<int:pk>/', ListingRetrieveUpdateDestroyView.as_view(), name='listing-detail'),
    path('listings/<int:pk>/view/', view_listing, name='listing-view'),
    path('listings/viewed/', ListingViewHistoryListView.as_view(), name='viewed-listings'),
]



