[![CI](https://github.com/tkhnhy/BibTex-Miniprojekti/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/tkhnhy/BibTex-Miniprojekti/actions/workflows/ci.yaml)

[**Product backlog + sprint backlogs**](https://helsinkifi-my.sharepoint.com/:x:/g/personal/hjhellen_ad_helsinki_fi/IQAvnQeKqT0uQYKpWgiyLJbaASYjHlJnmxERma5JgKgGz00)

# Installation

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

4. Initialize the database tables.
```bash
$ python src/db_helper.py
```

5. Run the Flask app.
```bash
$ poetry run python src/index.py
```
The application should now be running at ```http://localhost:5001/```.


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
- Test results and coverage are visible to the customer from the CI service.
