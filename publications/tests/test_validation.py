import pytest
from model_mommy import mommy

from publications.models import Article, Comment
from publications.api.serializers import CommentCreateSerializer


@pytest.mark.django_db
class TestCommentValidation:

    def test_forbidden_parent(self, profile_factory):
        profile = profile_factory.get()
        article = mommy.make(Article, author=profile)
        comment = mommy.make(Comment, author=profile, article=article)

        another_article = mommy.make(Article, author=profile)
        invalid_comment = mommy.make(Comment, author=profile,
                                     article=another_article,
                                     parent=comment)

        serializer = CommentCreateSerializer(data=invalid_comment.__dict__,
                                             context={'article': another_article})

        assert not serializer.is_valid()
        assert serializer.errors == {
            'parent_id': ['There is no such comment in this article.']}
