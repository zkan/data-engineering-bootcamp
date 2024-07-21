import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import (
    Addresses,
    Events,
    OrderItems,
    Orders,
    Products,
    Promos,
    Users,
)
from .serializers import (
    AddressesSerializer,
    EventsSerializer,
    OrderItemsSerializer,
    OrdersSerializer,
    ProductsSerializer,
    PromosSerializer,
    UsersSerializer,
)


class AddressesViewSet(viewsets.ModelViewSet):
    queryset = Addresses.objects.all()
    serializer_class = AddressesSerializer


class EventFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date', lookup_expr="exact")

    class Meta:
        model = Events
        fields = ["created_at"]


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter


class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer


class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date', lookup_expr="exact")

    class Meta:
        model = Orders
        fields = ["created_at"]


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class PromosViewSet(viewsets.ModelViewSet):
    queryset = Promos.objects.all()
    serializer_class = PromosSerializer


class UserFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date', lookup_expr="exact")

    class Meta:
        model = Users
        fields = ["created_at"]


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
