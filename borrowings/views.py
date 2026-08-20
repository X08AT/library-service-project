from rest_framework import generics

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingListView(generics.ListAPIView):
    queryset = Borrowing.objects.select_related("book")
    serializer_class = BorrowingSerializer


class BorrowingRetrieveView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related("book")
    serializer_class = BorrowingDetailSerializer


class BorrowingCreateView(generics.CreateAPIView):
    serializer_class = BorrowingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
