from django.urls import path

from borrowings.views import (
    BorrowingListView,
    BorrowingRetrieveView,
    BorrowingCreateView,
)

app_name = "borrowings"

urlpatterns = [
    path("borrowings/", BorrowingListView.as_view(), name="borrowings"),
    path("borrowings/<int:pk>/", BorrowingRetrieveView.as_view(), name="borrowing"),
    path("borrowings/create/", BorrowingCreateView.as_view(), name="create_borrowing"),
]
