import random

from factory import Faker, Sequence
from factory.django import DjangoModelFactory

from api_atelier.clients.choices import RANDOM_SECTIONS_CHOICES
from api_atelier.clients.models import Client, Service


class ClientFactory(DjangoModelFactory):
    name = Faker("user_name")
    adress = Faker("city")
    phone = Sequence(lambda n: "123555%04d" % n)

    class Meta:
        model = Client


class ServiceFactory(DjangoModelFactory):
    name = Faker("user_name")
    price = Faker("pyint")
    section = random.choice(RANDOM_SECTIONS_CHOICES)

    class Meta:
        model = Service
