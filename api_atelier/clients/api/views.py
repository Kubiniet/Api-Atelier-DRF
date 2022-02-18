# Utils
from datetime import date, timedelta

from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from api_atelier.clients.api.serializers import (
    ClientSerializer,
    OrderSerializer,
    OrderServiceSerializer,
    ServiceSerializer,
)
from api_atelier.clients.choices import MONTHS
from api_atelier.clients.models import Client, Order, OrderService, Service


class ClientsViewSet(viewsets.GenericViewSet):
    model = Client
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ("name", "id", "adress")
    ordering_fields = ("name",)
    search_fields = ["name", "adress"]

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs["pk"])

    def list(self, request):
        data = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(data, many=True)
        data = {"total": self.get_queryset().count(), "rows": data.data}
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Cliente registrado correctamente!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response(
            {"message": "", "error": "Cliente no encontrado!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(
                instance=self.get_object().get(), data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Cliente actualizado correctamente!"},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"message": "", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, pk=None):
        if self.get_object().exists():
            self.get_object().get().delete()
            return Response(
                {"message": "Cliente eliminado correctamente!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "", "error": "Cliente no encontrado!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ServiceViewSet(viewsets.GenericViewSet):
    model = Service
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs["pk"])

    def list(self, request):
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        data = {"total": self.get_queryset().count(), "rows": data.data}
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Servicio registrado correctamente!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response(
            {"message": "", "error": "Servicio no encontrado!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(
                instance=self.get_object().get(), data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Servicio actualizado correctamente!"},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"message": "", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, pk=None):
        if self.get_object().exists():
            self.get_object().get().delete()
            return Response(
                {"message": "Servicio eliminado correctamente!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "", "error": "Servicio no encontrado!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AddToCartView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="Add service to the order with id",
                required=True,
                type=int,
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        id = request.data.get("id", None)
        if id is None:
            return Response(
                {"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )

        service = get_object_or_404(Service, id=id)
        order_item_qs = OrderService.objects.filter(service=service, ordered=False)

        if order_item_qs.exists():
            order_item = order_item_qs.first()
            order_item.quantity += 1
            order_item.save()
        else:
            order_item = OrderService.objects.create(
                service=service, ordered=False, quantity=1
            )

        order_qs = Order.objects.filter(ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if not order.service.filter(service__id=order_item.id).exists():
                order.service.add(order_item)
                return Response(
                    {"message": "Servicio añadido correctamente!"},
                    status=status.HTTP_200_OK,
                )

        else:
            order = Order.objects.create()
            order.service.add(order_item)
            return Response(
                {"message": "Servicio añadido correctamente!"},
                status=status.HTTP_200_OK,
            )


class RemoveFromCartView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="Add service to the order with id",
                required=True,
                type=int,
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        id = request.data.get("id", None)
        if id is None:
            return Response(
                {"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )

        service = get_object_or_404(Service, id=id)
        order_qs = Order.objects.filter(ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            order_item_qs = OrderService.objects.filter(service=service, ordered=False)

            if order_item_qs.exists():
                order_item = order_item_qs.first()
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    return Response(
                        {"message": "Cantidad de servicios actualizado!"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    order.service.remove(order_item)
                    return Response(
                        {"message": "Servicio removido correctamente!"},
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                    {"message": "No hay servicios en la orden!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"message": "No hay ninguna orden activa!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class OrderViewSet(viewsets.GenericViewSet):
    model = Order
    serializer_class = OrderSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = (
        "client__name",
        "paid",
    )
    ordering_fields = ("paid", "client__name")

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs["pk"])

    @action(detail=False, methods=["get"])
    def get_order(self, request):
        data = OrderService.objects.filter(ordered=False)
        data = OrderServiceSerializer(data, many=True)
        return Response(data.data)

    def list(self, request):
        data = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(data, many=True)
        data = {"total": self.get_queryset().count(), "rows": data.data}
        return Response(data)

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response(
            {"message": "", "error": "Orden no encontrada!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(
                instance=self.get_object().get(), data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Orden actualizada correctamente!"},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"message": "", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, pk=None):
        if self.get_object().exists():
            self.get_object().get().delete()
            return Response(
                {"message": "Orden eliminada correctamente!"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "", "error": "Orden no encontrada!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ChartAPIView(APIView):
    def get(request, *args, **kwargs):
        """Labels and values for bar chart of chart.js


        Returns:
            _list_ : _labels of months and profit of orders_
            _list_ : _values of profit_
            _int_ : _count of profit orders_
        """
        labels = MONTHS
        orders = []
        count = []
        amount = 0
        X = date.today()
        for i in range(13):
            amount = 0

            items = Order.objects.filter(paid=True, order_date__month=i).filter(
                order_date__lt=X + timedelta(days=93)
            )
            for item in items:
                amount += item.get_final_price()
            if items.exists():
                count.append(items.count())
                orders.append(amount)

        data = {"labels": labels[: len(orders)], "values": orders, "count": count}
        return Response(data)
