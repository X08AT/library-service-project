from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


@extend_schema(
    summary="List of Borrowings",
    description="List of all borrowings of library.",
    responses=BorrowingSerializer,
)
class BorrowingListView(generics.ListAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book")

        is_active = self.request.query_params.get("is_active")

        if is_active == "True":
            queryset = queryset.filter(actual_return_date__isnull=True)

        if is_active == "False":
            queryset = queryset.filter(actual_return_date__isnull=False)

        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id")

            if user_id:
                queryset = queryset.filter(user_id=user_id)

            return queryset

        return queryset.filter(user=self.request.user)


@extend_schema(
    summary="Retrieve Borrowing",
    description="Get details about borrowing",
    responses=BorrowingDetailSerializer,
)
class BorrowingRetrieveView(generics.RetrieveAPIView):
    serializer_class = BorrowingDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book")

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)


@extend_schema(
    summary="Create Borrowing",
    description="Create a borrowing",
    request=BorrowingCreateSerializer,
    responses=BorrowingCreateSerializer,
)
class BorrowingCreateView(generics.CreateAPIView):
    serializer_class = BorrowingCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    post=extend_schema(
        summary="Return a borrowing",
        description="Return book you borrowing.",
        responses={
            201: {"description": "Borrowing returned successfully."},
            400: {"description": "You have already returned this borrowing."},
            401: {"description": "Authentication required."},
        },
    )
)
class BorrowingReturnView(APIView):
    def post(self, request, pk):
        borrowing = get_object_or_404(Borrowing, pk=pk)

        if borrowing.actual_return_date is not None:
            return Response(
                {"error": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            borrowing.actual_return_date = timezone.now().date()
            borrowing.save()

            book = borrowing.book
            book.inventory += 1
            book.save()

        return Response(
            {"message": "Book returned successfully."},
            status=status.HTTP_200_OK,
        )
