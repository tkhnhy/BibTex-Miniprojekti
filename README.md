[**Product backlog + sprint backlogs**](https://docs.google.com/spreadsheets/d/19QThnVXlWBjx3oyx5Rj04DEQLzPrbDfF0EEGH8a7vgo/edit?usp=sharing)

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
