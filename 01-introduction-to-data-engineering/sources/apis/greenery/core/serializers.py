from rest_framework import serializers

from .models import (
    Addresses,
    Events,
    OrderItems,
    Orders,
    Products,
    Promos,
    Users,
)


class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = "__all__"


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = "__all__"


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class PromosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promos
        fields = "__all__"


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"
