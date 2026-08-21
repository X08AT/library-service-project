from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

USER_URL = reverse("users:create")
ME_URL = reverse("users:manage")


class UnauthenticatedUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        payload = {
            "username": "testuser",
            "email": "test@mail.com",
            "password": "test123",
        }

        response = self.client.post(USER_URL, payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(get_user_model().objects.filter(username="testuser").exists())

    def test_user_registration_with_existing_username(self):
        get_user_model().objects.create_user(
            username="existing",
            email="test@mail.com",
            password="test123",
        )

        payload = {
            "username": "existing",
            "email": "test2@mail.com",
            "password": "test123",
        }

        response = self.client.post(USER_URL, payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_user_me_requires_authentication(self):
        response = self.client.get(ME_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class AuthenticatedUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@mail.com",
            password="test123",
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_current_user(self):
        response = self.client.get(ME_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["username"],
            self.user.username,
        )

    def test_update_current_user(self):
        payload = {
            "username": "updateduser",
            "email": "updated@mail.com",
            "password": "test123",
        }

        response = self.client.put(ME_URL, payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.username,
            "updateduser",
        )
        self.assertEqual(
            self.user.email,
            "updated@mail.com",
        )

    def test_partial_update_current_user(self):
        payload = {
            "username": "updateduser",
        }

        response = self.client.patch(ME_URL, payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.username,
            "updateduser",
        )
