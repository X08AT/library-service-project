from celery import shared_task

from borrowings.services.borrowings import get_overdue_borrowings
from borrowings.services.telegram import send_telegram_message


@shared_task
def check_overdue_borrowings():
    overdue_borrowings = get_overdue_borrowings()

    if not overdue_borrowings:
        send_telegram_message("No borrowings overdue today!")
        return

    for borrowing in overdue_borrowings:
        send_telegram_message(
            f"Overdue borrowing!\n"
            f"Book: {borrowing.book.title}\n"
            f"User: {borrowing.user.username}\n"
            f"Borrow date: {borrowing.borrow_date}\n"
            f"Expected return date: {borrowing.expected_return_date}"
        )
