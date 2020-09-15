from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from posts.filters import LikeFilter, PostFilter
from posts.models import Like, Post
from posts.serializers import LikeSerializer, PostSerializer


class PostCreationView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer

    def create(self, request):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        instance.created_by = self.request.user
        instance.save(
            update_fields=[
                "created_by",
            ]
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class PostView(generics.RetrieveAPIView):
    """
    Retrieve a single post by id.
    There is no update/delete functionality to save time.
    """

    serializer_class = PostSerializer
    lookup_url_kwarg = "id"

    def get_object(self):
        return (
            Post.objects.prefetch_related("likes")
            .filter(id=self.kwargs.get(self.lookup_url_kwarg))
            .first()
        )

    def retrieve(self, *args, **kwargs):
        serializer = self.serializer_class(instance=self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostListView(generics.ListAPIView):
    # pagination_class = LimitOffsetPagination
    queryset = Post.objects.prefetch_related("likes").all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = PostSerializer
    filterset_class = PostFilter


class LikeListView(generics.ListAPIView):
    # pagination_class = LimitOffsetPagination
    queryset = Like.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = LikeSerializer
    filterset_class = LikeFilter


class PostLikeView(generics.CreateAPIView):
    """
    Add/remove like on post by post id.
    """

    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "id"
    serializer_class = PostSerializer

    def get_object(self):
        return (
            Post.objects.prefetch_related("likes")
            .filter(id=self.kwargs.get(self.lookup_url_kwarg))
            .first()
        )

    def create(self, *args, **kwargs):
        post = self.get_object()
        is_liked = any(
            [like for like in post.likes.all() if like.created_by == self.request.user]
        )

        if is_liked:
            like = post.likes.filter(created_by=self.request.user).first()
            post.likes.remove(like)
            like.delete()

        else:
            like = Like.objects.create(created_by=self.request.user)
            post.likes.add(like)

        serializer = self.serializer_class(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)
