import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import force_authenticate

from bookmarks.models import ArticleBookmark


@pytest.mark.django_db
@pytest.mark.usefixtures('client')
class TestArticleBookmarkViews:

    def test_change_bookmark(self, profile_factory):
        profile = profile_factory.get()
        article = mommy.make('publications.Article', author=profile)

        self.client.force_authenticate(user=profile.user)

        url = reverse('article-bookmark-change',
                      kwargs={'pk': profile.id, 'article_pk': article.id})

        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert ArticleBookmark.objects.get()

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(ObjectDoesNotExist):
            ArticleBookmark.objects.get()
