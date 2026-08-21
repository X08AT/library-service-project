from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets

from books.models import Book
from books.permissions import IsAdminOrListOnly
from books.serializers import BookSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Books",
        description="List of all Books in library.",
        responses=BookSerializer,
    ),
    create=extend_schema(
        summary="Create Book",
        description="Create a new Book.",
        request=BookSerializer,
        responses=BookSerializer,
    ),
    update=extend_schema(
        summary="Update Book",
        description="Update a existing Book.",
        request=BookSerializer,
        responses=BookSerializer,
    ),
    partial_update=extend_schema(
        summary="Partial Update Book",
        description="Partial a existing Book.",
        request=BookSerializer,
        responses=BookSerializer,
    ),
    retrieve=extend_schema(
        summary="Retrieve Book",
        description="Retrieve a existing Book.",
        responses=BookSerializer,
    ),
    destroy=extend_schema(
        summary="Destroy Book",
        description="Destroy a existing Book.",
        responses=None,
    ),
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrListOnly]
