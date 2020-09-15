from django_filters import FilterSet, filters

from posts.models import Like, Post


class PostFilter(FilterSet):
    date_from = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Post
        fields = ("created_at",)


class LikeFilter(FilterSet):
    date_from = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Like
        fields = ("created_at",)
