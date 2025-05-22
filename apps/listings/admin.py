from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price','rooms','property_type',
                    'is_active', 'created_at', 'owner')
    search_fields = ('title', 'city', 'description')
    list_filter = ('city','property_type','is_active', 'created_at','rooms')
    list_editable = ('is_active',)
    ordering = ('-created_at',)