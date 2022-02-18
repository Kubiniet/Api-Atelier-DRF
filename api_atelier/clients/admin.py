from django.contrib import admin

from api_atelier.clients.models import Client, Order, OrderService, Service

admin.site.register(Client)
admin.site.register(Service)
admin.site.register(OrderService)
admin.site.register(Order)
