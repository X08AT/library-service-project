from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from books.models import Book
from books.serializers import BookSerializer

BOOK_URL = reverse("books:book-list")


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


def detail_book(book_id):
    return reverse("books:book-detail", kwargs={"pk": book_id})


class UnauthenticatedBookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required_for_list(self):
        response = self.client.get(BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthenticatedBookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@mail.com", password="test123"
        )
        self.client.force_authenticate(self.user)

    def test_books_list(self):
        sample_book()
        sample_book(author="Author2")
        response = self.client.get(BOOK_URL)

        books = Book.objects.all()

        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        book = sample_book()
        response = self.client.get(detail_book(book.id))

        serializer = BookSerializer(book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_book_create_forbidden(self):
        payload = {
            "title": "Sample Book",
            "author": "Author",
            "cover": Book.Cover.HARD,
            "inventory": 5,
            "daily_fee": 2,
        }
        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_update_forbidden(self):
        book = sample_book()
        payload = {
            "title": "Sample Book2",
        }
        response = self.client.patch(detail_book(book.id), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_delete_forbidden(self):
        book = sample_book()
        response = self.client.delete(detail_book(book.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@mail.com",
            password="test123",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_admin_create_book(self):
        payload = {
            "title": "Sample Book",
            "author": "Author",
            "cover": Book.Cover.HARD,
            "inventory": 5,
            "daily_fee": 2,
        }
        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="Sample Book").exists())

    def test_admin_update_book(self):
        book = sample_book()
        payload = {
            "title": "Sample Book2",
        }
        response = self.client.patch(detail_book(book.id), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Book.objects.filter(title="Sample Book2").exists())

    def test_admin_delete_book(self):
        book = sample_book()
        response = self.client.delete(detail_book(book.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(title="Sample Book").exists())
