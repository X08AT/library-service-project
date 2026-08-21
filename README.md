# Library Service Project

Library Service is a REST API for an online library. It allows users to browse available books, borrow and return books, while administrators can manage the library's book collection.

The project also integrates Telegram notifications for borrowing events and overdue borrowings.

## Environment Variables

Create a .env file based on .env.sample.

## Running the Project with Docker

Build and start the containers:

docker compose up --build

### Run the test suite with:

docker compose run --rm app python manage.py test