from django.urls import path

from .views import AddToCartView, ChartAPIView, RemoveFromCartView

urlpatterns = [
    path("add_service/", AddToCartView.as_view(), name="add-service"),
    path("remove_service/", RemoveFromCartView.as_view(), name="remove-service"),
    path("chart/", ChartAPIView.as_view(), name="chart"),
]
