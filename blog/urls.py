from django.urls import path
from .views import PostsListView, PostCreateView, PostUpdateView, PostDetailView

urlpatterns = [
    path("", PostsListView.as_view(), name="posts_list"),
    path("add/", PostCreateView.as_view(), name="post_add"),
    path("<int:pk>/", PostsListView.as_view()),
    path("update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    path('<int:pk>/signed_post',PostDetailView.as_view(), name='signed_post')
]
