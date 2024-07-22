from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()


def get_posts(user: User):
    if user.is_authenticated:
        return Post.objects.select_related('author')

    return Post.objects.select_related('author').filter(is_closed=False)
