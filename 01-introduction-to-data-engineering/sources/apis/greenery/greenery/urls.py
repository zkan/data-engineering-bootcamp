"""
URL configuration for greenery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from core import views


router = DefaultRouter()
router.register(r"addresses", views.AddressesViewSet, basename="addresses")
router.register(r"events", views.EventsViewSet, basename="events")
router.register(r"order-items", views.OrderItemsViewSet, basename="order-items")
router.register(r"orders", views.OrdersViewSet, basename="orders")
router.register(r"products", views.ProductsViewSet, basename="products")
router.register(r"promos", views.PromosViewSet, basename="promos")
router.register(r"users", views.UsersViewSet, basename="users")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
