from django.urls import path

from posts.views import (
    LikeListView,
    PostCreationView,
    PostLikeView,
    PostListView,
    PostView,
)

urlpatterns = [
    path("create/", PostCreationView.as_view(), name="post_create"),
    path("view/<int:id>/", PostView.as_view(), name="post_view"),
    path("like/<int:id>/", PostLikeView.as_view(), name="post_like"),
    path("posts/", PostListView.as_view(), name="post_list"),
    path("likes/", LikeListView.as_view(), name="post_like_list"),
]
