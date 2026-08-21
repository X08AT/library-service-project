from django.db import IntegrityError
from django.test import TestCase

from books.models import Book


class BookModelTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Book title",
            author="Author",
            cover=Book.Cover.HARD,
            inventory=5,
            daily_fee=2,
        )

    def test_book_str(self):
        self.assertEqual(str(self.book), self.book.title)

    def test_cannot_create_book_with_same_title_and_author(self):
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title="Book title",
                author="Author",
                cover=Book.Cover.SOFT,
                inventory=6,
                daily_fee=3,
            )
