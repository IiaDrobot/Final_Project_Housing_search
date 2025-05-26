from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['listing', 'tenant','get_user', 'start_date', 'end_date', 'created_at']
    list_filter = ['start_date', 'end_date']
    search_fields = ['tenant__email', 'listing__title']

    def get_user(self, obj):
        return obj.tenant.username
    get_user.short_description = 'Арендатор'
