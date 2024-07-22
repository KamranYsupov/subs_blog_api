from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .mixins import PostAPIViewMixin
from .permissions import IsOwnerOrReadOnly, IsAuthor
from .serializers import PostSerializer
from ..models import Post
from ..utils import get_posts


class PostListView(ListAPIView, ):
    pagination_class = PageNumberPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        return get_posts(self.request.user)


class DetailPostAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def get_queryset(self):
        return get_posts(self.request.user)


class CreatePostAPIView(CreateAPIView):
    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsAuthor)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


