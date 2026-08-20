from rest_framework import generics

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingListView(generics.ListAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
