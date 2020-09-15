from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UsersTests(APITestCase):
    create_url = reverse("user-list")
    login_url = reverse("jwt-create")
    activity_url = reverse("get_activity")

    data = {
        "username": "testuser",
        "password": "testpassword",
    }

    def authenticate(self):
        user = get_user_model().objects.create_user("test")
        self.client.force_authenticate(user)

    def test_registration_and_login(self):
        response = self.client.post(self.create_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        login_response = self.client.post(self.login_url, data=self.data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        user = User.objects.get(username=self.data.get("username"))

        self.assertTrue(user.check_password(self.data.get("password")))

    def test_activity(self):
        self.authenticate()

        # need to call twice so the request gets logged properly
        self.client.get(self.activity_url)
        response = self.client.get(self.activity_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("last_login"), str(date.today()))
