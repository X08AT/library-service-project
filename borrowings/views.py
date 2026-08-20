from rest_framework import generics

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingDetailSerializer


class BorrowingListView(generics.ListAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer


class BorrowingRetrieveView(generics.RetrieveAPIView):
    serializer_class = BorrowingDetailSerializer

    def get_object(self):
        return Borrowing.objects.get(pk=self.kwargs["pk"])
