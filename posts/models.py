from django.db import models

from users.models import User


class Like(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Post(models.Model):
    title = models.CharField(blank=False, max_length=255)
    body = models.TextField(blank=True, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(Like, related_name="post")

    class Meta:
        ordering = ["-created_at"]
