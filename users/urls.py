from django.urls import path

from users.views import ViewActivity

urlpatterns = [
    path("activity/", ViewActivity.as_view(), name="get_activity"),
]
