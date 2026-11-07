from rest_framework import viewsets

from .models import Booking, MenuItem
from .serializers import BookingSerializer, MenuItemSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.order_by("id")
    serializer_class = MenuItemSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.order_by("booking_date", "id")
    serializer_class = BookingSerializer
