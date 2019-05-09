import pytest
from django.contrib.auth import get_user_model
from model_mommy import mommy
from rest_framework.test import APIClient


@pytest.fixture
def profile_factory(db):
    class ProfileFactory:
        def get(self):
            return mommy.make(get_user_model()).profile
    return ProfileFactory()


@pytest.fixture(scope='class')
def client(request):
    request.cls.client = APIClient()
