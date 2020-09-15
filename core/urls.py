from django.contrib import admin
from django.urls import include, path

from posts import urls as posts_urls
from users import urls as user_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("api/me/", include(user_urls)),
    path("api/posts/", include(posts_urls)),
]
