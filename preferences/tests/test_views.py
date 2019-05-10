import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from preferences.models import (CategoryPreference, ProfilePreference,
                                ThemePreference)


@pytest.mark.django_db
@pytest.mark.usefixtures('client')
class TestThemePreferenceViews:

    def test_change_preference(self, profile_factory):
        profile = profile_factory.get()
        theme = mommy.make('tags.Theme')

        self.client.force_authenticate(user=profile.user)

        url = reverse('theme-preference-change',
                      kwargs={'pk': profile.id, 'theme_pk': theme.id})

        response = self.client.post(url, {'display': True})
        assert response.status_code == status.HTTP_200_OK
        assert ThemePreference.objects.get()

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(ObjectDoesNotExist):
            ThemePreference.objects.get()


@pytest.mark.django_db
@pytest.mark.usefixtures('client')
class TestCategoryPreferenceViews:

    def test_change_preference(self, profile_factory):
        profile = profile_factory.get()
        category = mommy.make('tags.Category')

        self.client.force_authenticate(user=profile.user)

        url = reverse('category-preference-change',
                      kwargs={'pk': profile.id, 'category_pk': category.id})

        response = self.client.post(url, {'display': True})
        assert response.status_code == status.HTTP_200_OK
        assert CategoryPreference.objects.get()

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(ObjectDoesNotExist):
            CategoryPreference.objects.get()


@pytest.mark.django_db
@pytest.mark.usefixtures('client')
class TestProfilePreferenceViews:

    def test_change_preference(self, profile_factory):
        profile = profile_factory.get()
        another_profile = profile_factory.get()

        self.client.force_authenticate(user=profile.user)

        url = reverse('profile-preference-change',
                      kwargs={'pk': profile.id, 'profile_pk': profile.id})

        response = self.client.post(url, {'display': True})
        assert response.status_code == status.HTTP_200_OK
        assert ProfilePreference.objects.get()

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(ObjectDoesNotExist):
            ProfilePreference.objects.get()
