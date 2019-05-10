import pytest
from model_mommy import mommy
from django.urls import reverse
from rest_framework import status

from publications.models import Article, Comment


@pytest.mark.django_db
@pytest.mark.usefixtures('client')
class TestCommentViews:

    def test_comment_list(self, profile_factory):
        profile = profile_factory.get()
        article = mommy.make(Article, author=profile)
        comment = mommy.make(Comment, author=profile, article=article)
        comment_reply = mommy.make(Comment, author=profile,
                                   article=article,
                                   parent=comment)

        self.client.force_authenticate(user=profile.user)

        url = reverse('article-comment-list',
                      kwargs={'article_pk': article.id})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert comment.id in map(lambda i: i['id'], response.data['results'])

        response = self.client.get(url, {'parent_id': comment.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert comment_reply.id in map(lambda i: i['id'],
                                       response.data['results'])

        response = self.client.get(url, {'parent_id': comment_reply.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0
