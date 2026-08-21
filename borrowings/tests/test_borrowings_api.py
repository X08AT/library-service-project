from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingDetailSerializer,
    BorrowingSerializer,
)

BORROWING_URL = reverse("borrowings:borrowings")
CREATE_BORROWING_URL = reverse("borrowings:create_borrowing")


def sample_book(**params):
    defaults = {
        "title": "Sample Book",
        "author": "Author",
        "cover": Book.Cover.HARD,
        "inventory": 5,
        "daily_fee": 2,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def sample_borrowing(user, book, **params):
    defaults = {
        "borrow_date": timezone.localdate(),
        "expected_return_date": (timezone.localdate() + timedelta(days=7)),
    }
    defaults.update(params)

    return Borrowing.objects.create(
        user=user,
        book=book,
        **defaults,
    )


def detail_borrowing(borrowing_id):
    return reverse(
        "borrowings:borrowing",
        kwargs={"pk": borrowing_id},
    )


def return_borrowing(borrowing_id):
    return reverse(
        "borrowings:return_borrowing",
        kwargs={"pk": borrowing_id},
    )


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_borrowings_list(self):
        response = self.client.get(BORROWING_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@mail.com",
            password="test123",
        )

        self.client.force_authenticate(self.user)

    def test_borrowings_list(self):
        book = sample_book()
        sample_borrowing(
            user=self.user,
            book=book,
        )
        sample_borrowing(
            user=self.user,
            book=book,
        )

        response = self.client.get(BORROWING_URL)

        borrowings = Borrowing.objects.all()

        serializer = BorrowingSerializer(
            borrowings,
            many=True,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data,
            serializer.data,
        )
        self.assertEqual(len(borrowings), 2)

    def test_borrowings_list_does_not_include_other_users_borrowings(
        self,
    ):
        book = sample_book()

        sample_borrowing(
            user=self.user,
            book=book,
        )

        other_user = get_user_model().objects.create_user(
            username="otheruser",
            email="other@test.com",
            password="test123",
        )

        sample_borrowing(
            user=other_user,
            book=book,
        )

        response = self.client.get(BORROWING_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)

    def test_retrieve_borrowing(self):
        book = sample_book()
        borrowing = sample_borrowing(
            user=self.user,
            book=book,
        )

        response = self.client.get(detail_borrowing(borrowing.id))

        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data,
            serializer.data,
        )

    def test_cannot_retrieve_other_user_borrowing(self):
        book = sample_book()

        other_user = get_user_model().objects.create_user(
            username="otheruser",
            email="other@test.com",
            password="test123",
        )

        borrowing = sample_borrowing(
            user=other_user,
            book=book,
        )

        response = self.client.get(detail_borrowing(borrowing.id))

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_create_borrowing(self):
        book = sample_book()

        payload = {
            "borrow_date": timezone.localdate(),
            "expected_return_date": (timezone.localdate() + timedelta(days=7)),
            "book": book.id,
        }

        response = self.client.post(
            CREATE_BORROWING_URL,
            payload,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        borrowing = Borrowing.objects.get(
            book=book,
            user=self.user,
        )

        self.assertEqual(borrowing.user, self.user)

    def test_filter_active_borrowings(self):
        book = sample_book()

        active_borrowing = sample_borrowing(
            user=self.user,
            book=book,
        )

        sample_borrowing(
            user=self.user,
            book=book,
            actual_return_date=timezone.localdate(),
        )

        response = self.client.get(
            BORROWING_URL,
            {"is_active": "True"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            active_borrowing.id,
        )

    def test_filter_inactive_borrowings(self):
        book = sample_book()

        sample_borrowing(
            user=self.user,
            book=book,
        )

        returned_borrowing = sample_borrowing(
            user=self.user,
            book=book,
            actual_return_date=timezone.localdate(),
        )

        response = self.client.get(
            BORROWING_URL,
            {"is_active": "False"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            returned_borrowing.id,
        )

    def test_return_borrowing(self):
        book = sample_book(inventory=4)

        borrowing = sample_borrowing(
            user=self.user,
            book=book,
        )

        response = self.client.post(return_borrowing(borrowing.id))

        borrowing.refresh_from_db()
        book.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIsNotNone(borrowing.actual_return_date)

        self.assertEqual(
            book.inventory,
            5,
        )

    def test_cannot_return_borrowing_twice(self):
        book = sample_book()

        borrowing = sample_borrowing(
            user=self.user,
            book=book,
            actual_return_date=timezone.localdate(),
        )

        response = self.client.post(return_borrowing(borrowing.id))

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            response.data["error"],
            "This borrowing has already been returned.",
        )


class AdminBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = get_user_model().objects.create_user(
            username="admin",
            email="admin@test.com",
            password="test123",
            is_staff=True,
        )

        self.client.force_authenticate(self.admin)

    def test_admin_can_see_all_borrowings(self):
        book = sample_book()

        user1 = get_user_model().objects.create_user(
            username="user1",
            email="user1@test.com",
            password="test123",
        )

        user2 = get_user_model().objects.create_user(
            username="user2",
            email="user2@test.com",
            password="test123",
        )

        sample_borrowing(
            user=user1,
            book=book,
        )

        sample_borrowing(
            user=user2,
            book=book,
        )

        response = self.client.get(BORROWING_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 2)

    def test_admin_can_filter_borrowings_by_user(self):
        book = sample_book()

        user1 = get_user_model().objects.create_user(
            username="user1",
            email="user1@test.com",
            password="test123",
        )

        user2 = get_user_model().objects.create_user(
            username="user2",
            email="user2@test.com",
            password="test123",
        )

        borrowing1 = sample_borrowing(
            user=user1,
            book=book,
        )

        sample_borrowing(
            user=user2,
            book=book,
        )

        response = self.client.get(
            BORROWING_URL,
            {"user_id": user1.id},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            borrowing1.id,
        )
