from django.db import models

from .choices import SECTIONS_CHOICES


class Client(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre")
    adress = models.CharField(max_length=30, verbose_name="Direccion")
    email = models.EmailField(blank=True, null=True, verbose_name="Correo")
    phone = models.CharField(max_length=10, null=True, verbose_name="Telefono")
    phone2 = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="2do telefono"
    )

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    section = models.CharField(choices=SECTIONS_CHOICES, max_length=2)

    def __str__(self):
        section = self.get_section_display()
        return str(f" {section} {self.name} ")


class OrderService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.service.name} x {self.quantity} "

    def get_total_price(self):
        return self.quantity * self.service.price


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateField(auto_now=True)
    service = models.ManyToManyField(OrderService)
    ordered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    extra_price = models.FloatField(default=0)

    def get_final_price(self):
        total = 0
        for order_item in self.service.all():
            total += order_item.get_total_price()
            if self.extra_price:
                total += self.extra_price
        return total

    def get_delivery_time(self):
        time = self.start_date.date()
        days = self.order_date
        res = days - time

        return res.days

    class Meta:
        ordering = ["-start_date"]
