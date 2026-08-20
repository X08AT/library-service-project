from django.urls import path

from borrowings.views import BorrowingListView, BorrowingRetrieveView

app_name = "borrowings"

urlpatterns = [
    path("borrowings/", BorrowingListView.as_view(), name="borrowings"),
    path("borrowings/<int:pk>/", BorrowingRetrieveView.as_view(), name="borrowing"),
]
