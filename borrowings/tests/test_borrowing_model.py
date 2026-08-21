from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from books.models import Book
from borrowings.models import Borrowing


class BorrowingModelTests(TestCase):
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
        self.borrowing = Borrowing.objects.create(
            borrow_date=timezone.localdate(),
            expected_return_date=timezone.localdate() + timedelta(days=1),
            book=self.book,
            user=self.user,
        )

    def test_borrowing_str(self):
        self.assertEqual(
            str(self.borrowing),
            f"Borrow date: {self.borrowing.borrow_date}, "
            f"Expected return date: {self.borrowing.expected_return_date}, "
            f"Returned: {self.borrowing.actual_return_date}",
        )

    def test_cannot_create_borrowing_with_expected_return_date_before_borrowing_date(
        self,
    ):
        with self.assertRaises(IntegrityError):
            Borrowing.objects.create(
                borrow_date=timezone.localdate(),
                expected_return_date=timezone.localdate() - timedelta(days=1),
                book=self.book,
                user=self.user,
            )

    def test_cannot_create_borrowing_with_actual_return_date_before_borrowing_date(
        self,
    ):
        with self.assertRaises(IntegrityError):
            Borrowing.objects.create(
                borrow_date=timezone.localdate(),
                expected_return_date=timezone.localdate() + timedelta(days=1),
                actual_return_date=timezone.localdate() - timedelta(days=2),
                book=self.book,
                user=self.user,
            )
