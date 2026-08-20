from django.db import models
from django.db.models import Q, F

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")

    class Meta:
        ordering = ["-borrow_date"]
        constraints = [
            models.CheckConstraint(
                condition=Q(expected_return_date__gte=F("borrow_date")),
                name="expected_return_after_borrow",
            ),
            models.CheckConstraint(
                condition=(
                    Q(actual_return_date__isnull=True)
                    | Q(actual_return_date__gte=F("borrow_date"))
                ),
                name="actual_return_after_borrow",
            ),
        ]

    def __str__(self):
        return (
            f"Borrow date: {self.borrow_date}, "
            f"Expected return date: {self.expected_return_date}, "
            f"Returned: {self.actual_return_date}"
        )
