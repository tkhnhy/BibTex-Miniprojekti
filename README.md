[![CI](https://github.com/tkhnhy/BibTex-Miniprojekti/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/tkhnhy/BibTex-Miniprojekti/actions/workflows/ci.yaml)

[**Product backlog + sprint backlogs**](https://helsinkifi-my.sharepoint.com/:x:/g/personal/hjhellen_ad_helsinki_fi/IQAvnQeKqT0uQYKpWgiyLJbaASYjHlJnmxERma5JgKgGz00)

# Installation on Linux

1. Clone the repository and navigate to the root folder.

2. Install dependencies using Poetry.
Check your [Poetry installation](https://python-poetry.org/docs/#installing-with-the-official-installer)
    with ```$ poetry --version```. 
    ```bash
    $ poetry install
    ```
    **Note:** This project requires python 3.12.

3. Create a ```.env``` file in the project root and configure the following environment variables.
    ```env
    SECRET_KEY=your_secret_key
    DATABASE_URL=postgresql://user:password@localhost:5432/my_db_name
    TEST_ENV=false
    ```
    Look [below](#creating-a-local-postgresql-database) for instructions on how create a local PostgreSQL database.

4. Start the virtual environment.
    ```bash
    $ eval $(poetry env activate)
    ```
    Then either first:
    * Initialize or clear the database tables.
    ```bash
    $ python src/db_helper.py
    ```
    Or straight away:
    * Run the Flask app using existing database entries.
    ```bash
    $ python src/index.py
    ```
    The application should now be running at ```http://localhost:5001/```.

5. Exit the application by pressing `Ctrl+C` while in the starting terminal and commanding `deactivate`.

## Creating a local PostgreSQL database

Assuming your username is "user". 
```bash
user$ sudo apt-get install postgresql
user$ sudo -u postgres bash
postgres$ createuser user
postgres$ createdb -O user my_db_name
postgres$ exit
```

Test:
```bash
user$ psql my_db_name
my_db_name=> \l+
q
my_db_name=> \q
```

Create a strong password using openssl command `openssl rand -base64 24` and use it to change/create user’s db-password: 
```bash
user$ sudo -u postgres psql
postgres$ ALTER USER user WITH PASSWORD 'new_password_from_openssl';
postgres$ exit
```
Test the database connection with the command `psql -U user -d my_db_name -h localhost` or in short `psql my_db_name`.


# Definition of Done

A user story, task, or feature is considered done when all of the following criteria are met:

Code Quality
- Code is properly formatted and passes Pylint checks.
- Naming is clear, meaningful, and consistent.
- Code is maintainable, and adheres to the project's architectural design.
- Inline comments added where necessary to clarify non-obvious logic.

Functionality
- Feature works as expected and fulfills all related acceptance criteria.
- Feature does not break existing functionality.
- No critical bugs or errors remain.

Testing
- Robot Framework tests are written according to the documented acceptance criteria.
- Automated unit tests are written where applicable, and test coverage is reasonable.
- All tests pass successfully.
- CI status is visible to the customer.

# About

The project was started using an OHTU [boilerplate](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate).
