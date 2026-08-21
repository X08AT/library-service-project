from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from books.models import Book
from borrowings.serializers import BorrowingSerializer


class BorrowingSerializersTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Book title",
            author="Author",
            cover=Book.Cover.HARD,
            inventory=5,
            daily_fee=2,
        )
        self.user = get_user_model().objects.create_user(
            username="user",
            email="test@mail.com",
            password="test123",
        )

    def test_cannot_borrow_book_if_inventory_is_empty(self):
        book = Book.objects.create(
            title="Book title2",
            author="Author",
            cover=Book.Cover.HARD,
            inventory=0,
            daily_fee=2,
        )
        serializer = BorrowingSerializer(
            data={
                "borrow_date": timezone.localdate(),
                "expected_return_date": timezone.localdate() + timedelta(days=1),
                "book": book,
                "user": self.user,
            }
        )
        self.assertFalse(serializer.is_valid())

    def test_cannot_borrow_book_if_expected_return_date_before_borrow_date(self):
        serializer = BorrowingSerializer(
            data={
                "borrow_date": timezone.localdate(),
                "expected_return_date": timezone.localdate() - timedelta(days=1),
                "book": self.book,
                "user": self.user,
            }
        )
        self.assertFalse(serializer.is_valid())
