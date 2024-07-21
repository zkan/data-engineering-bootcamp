from django.contrib import admin

from core.models import (
    Addresses,
    Events,
    OrderItems,
    Orders,
    Products,
    Promos,
    Users,
)


admin.site.register(Addresses)
admin.site.register(Events)
admin.site.register(OrderItems)
admin.site.register(Orders)
admin.site.register(Products)
admin.site.register(Promos)
admin.site.register(Users)
