from django.urls import path

from .views import PostListView, DetailPostAPIView, CreatePostAPIView


urlpatterns = [
    path('list/', PostListView.as_view(), name='posts_list'),
    path('create/', CreatePostAPIView.as_view(), name='create_post'),
    path('<int:pk>/', DetailPostAPIView.as_view(), name='detail_post')
]