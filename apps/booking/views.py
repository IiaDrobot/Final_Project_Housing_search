from rest_framework import viewsets, permissions, status
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import timedelta
from django.utils.timezone import now


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "TENANT":
            return Booking.objects.filter(tenant=user)
        elif user.role == "LESSOR":
            return Booking.objects.filter(listing__owner=user)
        return Booking.objects.none()

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save()  # tenant устанавливается в сериализаторе

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if request.user != booking.listing.owner:
            return Response({'error': 'Вы не владелец объявления.'}, status=status.HTTP_403_FORBIDDEN)

        if booking.status != Booking.Status.PENDING:
            return Response({'error': 'Можно подтвердить только заявки в ожидании.'}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = Booking.Status.CONFIRMED
        booking.save()
        return Response({'status': 'Бронирование подтверждено.'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def decline(self, request, pk=None):
        booking = self.get_object()
        if request.user != booking.listing.owner:
            return Response({'error': 'Вы не владелец объявления.'}, status=status.HTTP_403_FORBIDDEN)

        if booking.status != Booking.Status.PENDING:
            return Response({'error': 'Можно отклонить только заявки в ожидании.'}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = Booking.Status.DECLINED
        booking.save()
        return Response({'status': 'Бронирование отклонено.'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if request.user != booking.tenant:
            return Response({'error': 'Вы не арендатор этой брони.'}, status=status.HTTP_403_FORBIDDEN)

        if booking.status != Booking.Status.PENDING:
            return Response({'error': 'Можно отменить только заявки в ожидании.'}, status=status.HTTP_400_BAD_REQUEST)

        if booking.start_date - now().date() < timedelta(days=2):
            return Response({'error': 'Отменить бронирование можно не позднее, чем за 2 дня до заезда.'},
                            status=status.HTTP_400_BAD_REQUEST)

        booking.status = Booking.Status.CANCELLED
        booking.save()
        return Response({'status': 'Бронирование отменено арендатором.'})
