from rest_framework.views import APIView

from .serializers import PostSerializer
from posts.models import Post


class PostAPIViewMixin(APIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.select_related('author')

        return Post.objects.select_related('author').filter(is_closed=False)
