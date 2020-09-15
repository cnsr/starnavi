from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITransactionTestCase


class UsersTests(APITransactionTestCase):
    """
    These tests have to be ran with APITransactionTestCase.
    """

    create_url = reverse("post_create")
    # login_url = reverse("jwt-create")

    data = {
        "title": "Post Title",
        "body": "Post Body",
    }

    def authenticate(self):
        user = get_user_model().objects.create_user("test")
        self.client.force_authenticate(user)

    def create_post(self):
        return self.client.post(self.create_url, data=self.data)

    def test_create_post(self):
        self.authenticate()
        response = self.create_post()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), 1)
        self.assertEqual(response.data.get("title"), self.data.get("title"))
        self.assertEqual(response.data.get("body"), self.data.get("body"))

    def retrieve_created_post(self):
        self.authenticate()
        response = self.create_post()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), 1)

        self.retrieve_url = reverse("post_view", kwargs={"id": 1})

        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), 1)

    def test_like(self):
        self.authenticate()
        response = self.create_post()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # id is 2 since case is atomic
        self.assertEqual(response.data.get("id"), 2)

        self.like_url = reverse("post_like", kwargs={"id": 2})

        # like
        response = self.client.post(self.like_url)
        self.assertEqual(len(response.data.get("likes")), 1)

        # remove like
        response = self.client.post(self.like_url)
        self.assertEqual(len(response.data.get("likes")), 0)
