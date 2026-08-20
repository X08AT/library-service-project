from django.db import transaction
from rest_framework import serializers

from books.models import Book
from borrowings.models import Borrowing


class BookReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookReadSerializer(read_only=True)


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
        )

    def validate(self, attrs):
        if attrs["book"].inventory < 1:
            raise serializers.ValidationError({"book": "No books left."})
        if attrs["borrow_date"] > attrs["expected_return_date"]:
            raise serializers.ValidationError(
                {"expected_return_date": "Expected date must be after borrow date."}
            )
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            borrowing = super().create(validated_data)

            borrowing.book.inventory -= 1
            borrowing.book.save()

            return borrowing
