# Application Architecture

This document describes the architecture and workings of the BibTeX Reference Manager application. It is intended for developers who may be new to Flask app development.

## Table of Contents

1. [Overview](#overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Project Structure](#project-structure)
4. [Layer Structure](#layer-structure)
5. [Key Components](#key-components)
6. [Data Flow](#data-flow)
7. [Database Schema](#database-schema)
8. [Function Reference](#function-reference)

---

## Overview

The BibTeX Reference Manager is a Flask-based web application that allows users to:
- Create, view, edit, and delete bibliographic references
- Tag references for organization
- Filter references by type or tag
- Export references as BibTeX (.bib) files
- Import references from BibTeX files

The application follows a **layered architecture** with clear separation between:
- **Routes (Controllers)** – Handle HTTP requests and responses
- **Repositories (Data Access)** – Manage database operations
- **Entities (Models)** – Define data structures

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER BROWSER                               │
│                         (HTML Forms, JavaScript)                        │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │ HTTP Requests/Responses
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           FLASK APPLICATION                             │
│                              (index.py)                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      ROUTES (app.py)                              │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │  │
│  │  │ route_index │ │ route_new   │ │ route_edit  │ │ route_delete│  │  │
│  │  │     "/"     │ │ _reference  │ │ _reference  │ │ _reference  │  │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘  │  │
│  │  ┌─────────────┐ ┌─────────────┐                                  │  │
│  │  │ download_   │ │ upload_bib  │                                  │  │
│  │  │    bib      │ │             │                                  │  │
│  │  └─────────────┘ └─────────────┘                                  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                      │                                  │
│                                      │ uses                             │
│                                      ▼                                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     UTILITIES (util.py)                           │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ validate_reference() - validates user input before saving   │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                      │                                  │
│                                      │ calls                            │
│                                      ▼                                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                    REPOSITORIES (repositories/)                   │  │
│  │  ┌─────────────────────────┐  ┌─────────────────────────────────┐ │  │
│  │  │ reference_repository.py │  │ tag_repository.py               │ │  │
│  │  │ - get_references()      │  │ - get_tags_with_counts()        │ │  │
│  │  │ - create_reference()    │  │ - add_tags_to_reference()       │ │  │
│  │  │ - update_reference()    │  │ - delete_tags_from_reference()  │ │  │
│  │  │ - delete_reference()    │  │                                 │ │  │
│  │  │ - get_filtered_refs()   │  │                                 │ │  │
│  │  └─────────────────────────┘  └─────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                      │                                  │
│                                      │ uses                             │
│                                      ▼                                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      ENTITIES (entities/)                         │  │
│  │  ┌─────────────────────────┐  ┌───────────────────────────────┐   │  │
│  │  │ reference.py            │  │ tag.py                        │   │  │
│  │  │ - Reference class       │  │ - Tag class                   │   │  │
│  │  │ - ReferenceType enum    │  │                               │   │  │
│  │  │ - COMMON_BIBTEX_FIELDS  │  │                               │   │  │
│  │  └─────────────────────────┘  └───────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                      │                                  │
│                                      │ uses                             │
│                                      ▼                                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                    DATABASE (config.py, db_helper.py)             │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ Flask-SQLAlchemy + PostgreSQL                               │  │  │
│  │  │ - db = SQLAlchemy(app)                                      │  │  │
│  │  │ - reset_db(), setup_db()                                    │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        POSTGRESQL DATABASE                              │
│  ┌───────────────────┐ ┌──────────┐ ┌────────────────────────────────┐  │
│  │ reference_table   │ │ tags     │ │ reference_taggins (join table) │  │
│  └───────────────────┘ └──────────┘ └────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
src/
├── app.py                  # Main application routes (Flask controllers)
├── config.py               # Flask app configuration and database setup
├── db_helper.py            # Database initialization and reset utilities
├── index.py                # Application entry point
├── util.py                 # Validation utilities
├── schema.sql              # Database schema definition
│
├── entities/               # Data models (plain Python classes)
│   ├── reference.py        # Reference class and ReferenceType enum
│   └── tag.py              # Tag class
│
├── repositories/           # Data access layer (database operations)
│   ├── reference_repository.py  # CRUD operations for references
│   └── tag_repository.py        # CRUD operations for tags
│
├── templates/              # Jinja2 HTML templates
│   ├── layout.html         # Base template
│   ├── index.html          # Main page with reference list
│   ├── new_reference.html  # Form for creating references
│   ├── edit_reference.html # Form for editing references
│   └── delete_reference.html   # Deletion confirmation page
│
├── static/                 # Static assets (CSS, JavaScript)
│   └── style.css           # Application styles
│
├── tests/                  # Unit tests (pytest)
└── story_tests/            # End-to-end tests (Robot Framework)
```

---

## Layer Structure

The application follows a three-layer architecture:

### 1. Routes Layer (`app.py`)

The routes layer handles HTTP requests and responses. Each route:
- Receives user input from forms or URL parameters
- Validates input using utilities
- Calls repository functions to perform database operations
- Renders templates or redirects users

**Key Concept for Flask Beginners:**
Flask uses decorators like `@app.route("/")` to map URLs to Python functions. When a user visits `/`, Flask calls the decorated function and returns its response to the browser.

### 2. Repository Layer (`repositories/`)

The repository layer abstracts database operations. It:
- Contains functions for CRUD (Create, Read, Update, Delete) operations
- Uses SQLAlchemy's `text()` for raw SQL queries
- Converts database rows to entity objects
- Handles database transactions

**Key Concept:**
Repositories keep database logic separate from routes, making the code easier to test and maintain.

### 3. Entity Layer (`entities/`)

The entity layer defines data structures:
- `Reference`: Represents a bibliographic reference with id, key, type, content, tags, and comment
- `Tag`: Represents a tag that can be associated with references
- `ReferenceType`: An enum defining valid BibTeX entry types (article, book, etc.)

**Key Concept:**
Entities are simple Python classes that hold data. They don't contain database logic.

---

## Key Components

### `config.py` – Application Configuration

```python
app = Flask(__name__)              # Creates the Flask application
app.secret_key = getenv("SECRET_KEY")  # Required for session/flash messages
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)               # Database connection
```

This file initializes Flask and SQLAlchemy. The `db` object is imported throughout the application to interact with the database.

### `app.py` – Route Definitions

Main routes:
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET, POST | Display all references (with optional filters) |
| `/new_reference` | GET | Show form for creating a reference |
| `/create_reference` | POST | Save a new reference |
| `/edit_reference/<key>` | GET | Show form for editing a reference |
| `/save_edited_reference/<key>` | POST | Update a reference |
| `/confirm_delete/<key>` | GET | Show delete confirmation |
| `/delete_reference/<key>` | POST | Delete a reference |
| `/download_bib` | POST | Export references as .bib file |
| `/upload_bib` | POST | Import references from .bib file |

### `util.py` – Validation

The `validate_reference()` function checks:
- Citation key is not empty
- Citation key is unique
- Reference type is valid
- All required fields for the reference type are filled

### `entities/reference.py` – Reference Model

Key elements:
- `COMMON_BIBTEX_FIELDS`: List of all valid BibTeX field names
- `ReferenceType`: Enum with all BibTeX entry types
- `ReferenceType.field_requirements()`: Returns required fields for each type
- `Reference`: Class representing a reference with `__str__()` for BibTeX output
- `Reference.from_bibtex()`: Class method to parse BibTeX strings

### `repositories/reference_repository.py` – Reference Operations

Key functions:
- `get_references()`: Fetch all references with their tags
- `get_reference_by_key(key)`: Fetch one reference by its citation key
- `create_reference(...)`: Insert a new reference
- `update_reference(...)`: Update an existing reference
- `delete_reference(key)`: Delete a reference by key
- `get_filtered_references(filters)`: Fetch references matching type/tag filters

### `repositories/tag_repository.py` – Tag Operations

Key functions:
- `get_tags_with_counts()`: Get all tags with their reference counts
- `add_tags_to_reference(reference_id, tag_names)`: Associate tags with a reference
- `delete_tags_from_reference(reference_id)`: Remove tag associations

---

## Data Flow

### Creating a New Reference

```
1. User visits /new_reference
   └── route_new_reference() renders new_reference.html form

2. User fills form and submits
   └── POST to /create_reference

3. route_reference_creation():
   ├── Extract form data (type, key, content, tags)
   ├── validate_reference() checks input
   │   └── If invalid: flash error message, redirect back to form
   ├── create_reference() in repository
   │   ├── INSERT into reference_table
   │   └── add_tags_to_reference() inserts tags and links
   └── redirect to "/" (index page)

4. User sees updated reference list
```

### Viewing References with Filters

```
1. User visits /?reference_type[]=book&tag[]=science
   └── route_index() with filter parameters

2. route_index():
   ├── Parse filter parameters from request.args
   ├── get_filtered_references(filters)
   │   ├── Build dynamic SQL with WHERE clauses
   │   ├── Execute query
   │   └── Convert rows to Reference objects
   └── render_template("index.html", references=...)

3. Template displays filtered references
```

### Exporting to BibTeX

```
1. User selects references (checkboxes) and clicks "Download as BibTeX"
   └── JavaScript collects selected keys, submits form

2. download_bib():
   ├── Get selected_keys from form
   ├── get_references_by_keys(keys) or get_references()
   ├── For each reference: str(reference) produces BibTeX
   ├── Combine all into bibtex_content
   └── send_file() sends .bib file download

3. Browser downloads references.bib
```

---

## Database Schema

The application uses PostgreSQL with three tables:

```sql
-- Main table storing references
CREATE TABLE reference_table (
  id SERIAL PRIMARY KEY,
  reference_key TEXT UNIQUE NOT NULL,  -- Citation key (e.g., "Martin2009")
  reference_type TEXT NOT NULL,        -- Entry type (e.g., "book")
  reference_data JSONB NOT NULL,       -- Field data as JSON (author, title, etc.)
  comment TEXT DEFAULT ''              -- Optional comment (not part of BibTeX)
);

-- Tags for organizing references
CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL            -- Tag name (lowercase)
);

-- Many-to-many relationship between references and tags
CREATE TABLE reference_taggins (
  reference_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY (reference_id, tag_id),
  FOREIGN KEY (reference_id) REFERENCES reference_table(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
```

**Entity-Relationship Diagram:**

```
┌─────────────────────┐       ┌──────────────────────┐       ┌────────────┐
│   reference_table   │       │  reference_taggins   │       │    tags    │
├─────────────────────┤       ├──────────────────────┤       ├────────────┤
│ id (PK)             │◄──────┤ reference_id (FK)    │       │ id (PK)    │
│ reference_key       │       │ tag_id (FK)          │──────►│ name       │
│ reference_type      │       └──────────────────────┘       └────────────┘
│ reference_data      │              Many-to-Many
│ comment             │              Relationship
└─────────────────────┘
```

---

## Function Reference

### Routes (`app.py`)

| Function | Description |
|----------|-------------|
| `route_index()` | Displays all references, handles filtering by type and tag |
| `route_new_reference()` | Renders the create reference form |
| `route_reference_creation()` | Processes form submission to create a reference |
| `route_confirm_delete(key)` | Shows delete confirmation page |
| `route_delete_reference(key)` | Deletes a reference |
| `route_edit_reference(key)` | Renders the edit reference form |
| `route_save_edited_reference(key)` | Processes form submission to update a reference |
| `download_bib()` | Exports selected references as a .bib file |
| `upload_bib()` | Imports references from an uploaded .bib file |

### Repositories (`repositories/reference_repository.py`)

| Function | Description |
|----------|-------------|
| `row_to_reference(row)` | Converts a database row to a Reference object |
| `get_references()` | Returns all references with their tags |
| `get_references_by_keys(keys)` | Returns references matching the given keys |
| `get_reference_by_key(key)` | Returns a single reference by citation key |
| `create_reference(type, key, content, tags, comment)` | Inserts a new reference |
| `get_filtered_references(filters)` | Returns references matching type/tag filters |
| `delete_reference(key)` | Deletes a reference by citation key |
| `update_reference(...)` | Updates an existing reference |
| `add_ref_for_storytests()` | Helper for Robot Framework tests |

### Repositories (`repositories/tag_repository.py`)

| Function | Description |
|----------|-------------|
| `get_tags_with_counts()` | Returns all tags with their reference counts |
| `get_reference_tags(ref_id)` | Returns tags for a specific reference |
| `add_tags_to_reference(ref_id, names)` | Associates tags with a reference |
| `delete_tags_from_reference(ref_id)` | Removes all tags from a reference |

### Utilities (`util.py`)

| Function | Description |
|----------|-------------|
| `validate_reference(type, key, content, old_key)` | Validates reference data before saving |

### Entities (`entities/reference.py`)

| Class/Function | Description |
|----------------|-------------|
| `Reference` | Data class representing a bibliographic reference |
| `Reference.__str__()` | Converts reference to BibTeX format |
| `Reference.from_bibtex(id, bibtex_str)` | Parses a BibTeX string into a Reference |
| `ReferenceType` | Enum of valid BibTeX entry types |
| `ReferenceType.field_requirements()` | Returns required fields for the type |
| `ReferenceType.display_str()` | Returns human-readable type name |

### Database (`db_helper.py`)

| Function | Description |
|----------|-------------|
| `reset_db()` | Clears all data from tables |
| `setup_db()` | Drops and recreates database tables from schema.sql |
| `tables()` | Returns list of all table names in the database |

---

## Getting Started for New Developers

1. **Set up the environment** – Follow the installation instructions in README.md
2. **Understand the entry point** – `index.py` starts the Flask development server
3. **Trace a request** – Start with `route_index()` in `app.py` and follow the calls
4. **Run the tests** – Use `pytest` for unit tests and `run_robot_tests.sh` for end-to-end tests
5. **Explore templates** – See how data flows from Python to HTML in `templates/`

For any questions, refer to the [Flask documentation](https://flask.palletsprojects.com/).
