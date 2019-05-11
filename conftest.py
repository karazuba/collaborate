import pytest
from django.contrib.auth import get_user_model
from model_mommy import mommy
from rest_framework.test import APIClient


@pytest.fixture
def profile_factory(db):
    class ProfileFactory:
        def get(self, quantity=1):
            profiles = list(map(lambda u: u.profile,
                                mommy.make(get_user_model(), _quantity=quantity)))
            if len(profiles) == 1:
                return profiles[0]
            return profiles
    return ProfileFactory()


@pytest.fixture(scope='class')
def client(request):
    request.cls.client = APIClient()
