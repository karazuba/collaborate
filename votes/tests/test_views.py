import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from model_mommy import mommy

from votes.models import ArticleVote, CommentVote


@pytest.mark.django_db
@pytest.mark.usefixtures('client')
class TestArticleVoteViews:

    def test_make_vote(self, profile_factory):
        profile = profile_factory.get()
        article = mommy.make('publications.Article', author=profile)

        self.client.force_authenticate(user=profile.user)

        url = reverse('article-vote-make',
                      kwargs={'pk': profile.id, 'article_pk': article.id})

        response = self.client.post(url, {'value': True})
        assert ArticleVote.objects.get()

        response = self.client.post(url, {'value': False})
        with pytest.raises(ObjectDoesNotExist):
            ArticleVote.objects.get()

        response = self.client.post(url, {'value': False})
        assert ArticleVote.objects.get()


@pytest.mark.django_db
@pytest.mark.usefixtures('client')
class TestCommentVoteViews:

    def test_make_vote(self, profile_factory):
        profile = profile_factory.get()
        article = mommy.make('publications.Article', author=profile)
        comment = mommy.make('publications.Comment',
                             author=profile, article=article)

        self.client.force_authenticate(user=profile.user)

        url = reverse('comment-vote-make',
                      kwargs={'pk': profile.id, 'comment_pk': comment.id})

        response = self.client.post(url, {'value': True})
        assert CommentVote.objects.get()

        response = self.client.post(url, {'value': False})
        with pytest.raises(ObjectDoesNotExist):
            CommentVote.objects.get()

        response = self.client.post(url, {'value': False})
        assert CommentVote.objects.get()
