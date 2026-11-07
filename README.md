# Little Lemon • Back-End Developer Capstone

A Django REST Framework service for the Little Lemon restaurant. Staff can maintain menu items and table reservations. Reviewers can register a local user and try the API in Insomnia or Django REST Framework's browsable interface.

See [Readme.txt](Readme.txt) for endpoint paths, authentication and example requests.

## Local setup

Use Python 3.12, Pipenv and a running MySQL 8.0.11+ server.

1. In a MySQL administrator session, provision a local database and account. Choose your own password.

   ```sql
   CREATE DATABASE littlelemon CHARACTER SET utf8mb4;
   CREATE USER 'littlelemon'@'localhost' IDENTIFIED BY 'choose-your-local-password';
   GRANT ALL PRIVILEGES ON littlelemon.* TO 'littlelemon'@'localhost';
   GRANT ALL PRIVILEGES ON test_littlelemon.* TO 'littlelemon'@'localhost';
   ```

2. Copy `.env.example` to `.env`. Set `MYSQL_PASSWORD` to the password from step 1. Change the host, port, user or database if needed.
3. From the directory containing `manage.py`, run:

   ```sh
   pipenv sync
   pipenv run python manage.py migrate
   pipenv run python manage.py test
   pipenv run python manage.py runserver
   ```

4. Open the [restaurant homepage](http://127.0.0.1:8000/). Use the registration endpoint in the API guide to create a user, then sign in from the homepage or obtain a token in Insomnia.

The test runner creates and removes a separate MySQL database. Tests exercise the menu model, static page and stylesheet, user registration, token login/logout, authorization, input validation and both CRUD APIs.
