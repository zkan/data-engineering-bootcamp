from django.db import models


class Addresses(models.Model):
    address_id = models.CharField(primary_key=True, max_length=256)
    address = models.CharField(max_length=8192, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses'


class Events(models.Model):
    event_id = models.CharField(primary_key=True, max_length=256)
    session_id = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    page_url = models.CharField(max_length=4096, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    event_type = models.CharField(max_length=128, blank=True, null=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Products', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'


class OrderItems(models.Model):
    order = models.OneToOneField('Orders', models.DO_NOTHING, primary_key=True)  # The composite primary key (order_id, product_id) found, that is not supported. The first column is selected.
    product = models.ForeignKey('Products', models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_items'
        unique_together = (('order', 'product'),)


class Orders(models.Model):
    order_id = models.CharField(primary_key=True, max_length=256)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    promo = models.ForeignKey('Promos', models.DO_NOTHING, blank=True, null=True)
    address = models.ForeignKey(Addresses, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    order_cost = models.FloatField(blank=True, null=True)
    shipping_cost = models.FloatField(blank=True, null=True)
    order_total = models.FloatField(blank=True, null=True)
    tracking_id = models.CharField(max_length=256, blank=True, null=True)
    shipping_service = models.CharField(max_length=128, blank=True, null=True)
    estimated_delivery_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Products(models.Model):
    product_id = models.CharField(primary_key=True, max_length=256)
    name = models.CharField(max_length=1024, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    inventory = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Promos(models.Model):
    promo_id = models.CharField(primary_key=True, max_length=256)
    discount = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'promos'


class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=256)
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=1024, blank=True, null=True)
    phone_number = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    address = models.ForeignKey(Addresses, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
