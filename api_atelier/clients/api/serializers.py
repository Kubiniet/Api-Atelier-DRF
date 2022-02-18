from drf_spectacular.utils import OpenApiTypes, extend_schema_field
from rest_framework import serializers

from api_atelier.clients.models import Client, Order, OrderService, Service


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    section_display = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = "__all__"

    @extend_schema_field(OpenApiTypes.STR)
    def get_section_display(self, obj):
        return obj.get_section_display()


class OrderServiceSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderService
        fields = "__all__"

    @extend_schema_field(OpenApiTypes.STR)
    def get_service(self, obj):
        return ServiceSerializer(obj.service).data

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_total_price(self, obj):
        return obj.get_total_price()


class OrderSerializer(serializers.ModelSerializer):
    order_services = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    delivery_time = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "client",
            "client_name",
            "order_services",
            "extra_price",
            "total",
            "ordered",
            "paid",
            "delivery_time",
        )

    @extend_schema_field(OpenApiTypes.STR)
    def get_order_services(self, obj):
        return OrderServiceSerializer(obj.service.all(), many=True).data

    @extend_schema_field(OpenApiTypes.INT)
    def get_total(self, obj):
        return obj.get_final_price()

    @extend_schema_field(OpenApiTypes.INT)
    def get_delivery_time(self, obj):
        return obj.get_delivery_time()

    @extend_schema_field(OpenApiTypes.STR)
    def get_client_name(self, obj):
        if obj.client is not None:
            return obj.client.name
        else:
            return ""


class ChartSerializer(serializers.ListField):
    labels = serializers.CharField()
    data = serializers.CharField()
    count = serializers.CharField()
