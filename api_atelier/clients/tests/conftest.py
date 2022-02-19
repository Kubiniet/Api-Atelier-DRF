import pytest

from api_atelier.users.tests.factories import AdminFactory

from .factories import ClientFactory, ServiceFactory


@pytest.fixture
def admin_creation():
    return AdminFactory.create()


@pytest.fixture
def client_creation():
    return ClientFactory.create()


@pytest.fixture
def service_creation():
    return ServiceFactory.create()
