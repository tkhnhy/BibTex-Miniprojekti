import json
from sqlalchemy import text
from entities.reference import Reference, ReferenceType
from entities.tag import Tag
from repositories.tag_repository import add_tags_to_reference, delete_tags_from_reference
from config import db

def row_to_reference(row) -> Reference:
    return Reference(
        id_=row[0],
        key=row[1],
        type_=ReferenceType(row[2]),
        content=row[3],
        comment=row[4],
        tags=[Tag(name=name) for name in row[5]]
    )

def get_references(sort_by=None):
    allowed = {
        "author": "r.reference_data->>'author'",
        "year": "CAST(r.reference_data->>'year' AS INTEGER)",
        "key": "r.reference_key",
        "type": "r.reference_type",
    }
    order_sql = allowed.get(sort_by, "r.id")
    sql = text(
        f"""
        SELECT r.id, r.reference_key, r.reference_type, r.reference_data, r.comment,
               COALESCE(array_agg(DISTINCT t.name ORDER BY t.name) FILTER (WHERE t.name IS NOT NULL),
               ARRAY[]::text[]) AS tags
        FROM reference_table r
        LEFT JOIN reference_taggins rt ON rt.reference_id = r.id
        LEFT JOIN tags t ON t.id = rt.tag_id
        GROUP BY r.id
        ORDER BY {order_sql}
        """
    )
    rows = db.session.execute(sql).fetchall()
    return [row_to_reference(row) for row in rows]


def get_references_by_keys(keys: list[str], sort_by=None):
    if not keys:
        return []

    placeholders = ", ".join(f":k{i}" for i in range(len(keys)))
    params = {f"k{i}": keys[i] for i in range(len(keys))}
    allowed = {
    "author": "r.reference_data->>'author'",
    "year": "CAST(r.reference_data->>'year' AS INTEGER)",
    "key": "r.reference_key",
    "type": "r.reference_type",
}
    order_sql = allowed.get(sort_by, "r.id")
    sql = text(
        f"""
        SELECT r.id, r.reference_key, r.reference_type, r.reference_data, r.comment,
               COALESCE(array_agg(DISTINCT t.name ORDER BY t.name) FILTER (WHERE t.name IS NOT NULL),
               ARRAY[]::text[]) AS tags
        FROM reference_table r
        LEFT JOIN reference_taggins rt ON rt.reference_id = r.id
        LEFT JOIN tags t ON t.id = rt.tag_id
        WHERE r.reference_key IN ({placeholders})
        GROUP BY r.id
        ORDER BY {order_sql}
        """
    )
    rows = db.session.execute(sql, params).fetchall()
    return [row_to_reference(row) for row in rows]


def get_reference_by_key(key: str):
    sql = text(
        """
        SELECT r.id, r.reference_key, r.reference_type, r.reference_data, r.comment,
               COALESCE(array_agg(DISTINCT t.name ORDER BY t.name) FILTER (WHERE t.name IS NOT NULL),
               ARRAY[]::text[]) AS tags
        FROM reference_table r
        LEFT JOIN reference_taggins rt ON rt.reference_id = r.id
        LEFT JOIN tags t ON t.id = rt.tag_id
        WHERE r.reference_key = :key
        GROUP BY r.id
        """
    )
    row = db.session.execute(sql, {"key": key}).fetchone()
    if row is None:
        return None
    return row_to_reference(row)


def create_reference(reference_type: str, reference_key: str, reference_content: dict,
                     tags: list[str], comment: str = ''):
    sql = text(
        "INSERT INTO reference_table (reference_type, reference_key, reference_data, comment) "
        "VALUES (:reference_type, :reference_key, :reference_data, :comment) "
        "RETURNING id"
    )
    result = db.session.execute(sql, { "reference_type": reference_type, "reference_key": reference_key,
                             "reference_data": json.dumps(reference_content), "comment": comment})
    reference_id = result.fetchone()[0]
    add_tags_to_reference(reference_id, tags, commit=False)
    db.session.commit()

def year_to_sql_condition(year_input, column_name="(reference_data->>'year')::int"):
    # Types of input "2015", "<2000", ">2000", "2000-2010"
    year_input = year_input.strip()

    # Handle range
    if "-" in year_input:
        parts = year_input.split("-")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return f"{column_name} BETWEEN {parts[0]} AND {parts[1]}"

    # Handle < or >
    if year_input.startswith("<") or year_input.startswith(">"):
        operator = year_input[0]
        value = year_input[1:]
        if value.isdigit():
            return f"{column_name} {operator} {value}"

    # Handle exact year
    if year_input.isdigit():
        return f"{column_name} = {year_input}"

    # If input doesn't match known patterns
    raise ValueError(f"Invalid year input: {year_input}")

def id_search_any_field(word: str) -> set[int]:
    sql = text("""
        SELECT id
        FROM reference_table
        WHERE to_tsvector('english', reference_data::text)
              @@ plainto_tsquery(:word)
    """)

    return set(db.session.execute(sql, {"word": word}).scalars().all())

def id_search_specific_field(field: str, word: str) -> set[int]:
    if field in ("title", "author", "publisher"):

        sql = text(f"""
            SELECT id
            FROM reference_table
            WHERE unaccent(reference_data->>'{field}')
            ILIKE :pattern
            """)
        pattern = f"%{word}%"
        return set(db.session.execute(sql, {"pattern": pattern}).scalars().all())
    if field == "year":
        year_condition = year_to_sql_condition(word)

        sql = text(f"""
            SELECT id
            FROM reference_table
            WHERE {year_condition}
            """)

        return set(db.session.execute(sql).scalars().all())
    return {-1}
def id_search_keys_partial(substring: str) -> set[int]:
    sql = text("""
        SELECT id
        FROM reference_table
        WHERE reference_key ILIKE :pattern
    """)
    pattern = f"%{substring}%"
    return set(db.session.execute(sql, {"pattern": pattern}).scalars().all())

def get_filtered_references(filters, sort_by=None):
    allowed = {
    "author": "r.reference_data->>'author'",
    "year": "CAST(r.reference_data->>'year' AS INTEGER)",
    "key": "r.reference_key",
    "type": "r.reference_type",
    }
    
    order_sql = allowed.get(sort_by, "r.id")
    
    sql_parts = [
        "SELECT r.id, r.reference_key, r.reference_type, r.reference_data, r.comment,",
            "COALESCE(array_agg(DISTINCT t.name ORDER BY t.name) FILTER (WHERE t.name IS NOT NULL),",
            "ARRAY[]::text[]) AS tags",
        "FROM reference_table r",
        "LEFT JOIN reference_taggins rt ON rt.reference_id = r.id",
        "LEFT JOIN tags t ON t.id = rt.tag_id"
    ]
    where_clauses = []
    params = {}

    # Build WHERE clauses dynamically
    for filter_type, values in filters:
        if not values:
            continue

        param_name = f"{filter_type}_vals"

        if filter_type == "type":
            where_clauses.append(f"r.reference_type IN :{param_name}")
            params[param_name] = tuple(values)
        elif filter_type == "tag":
            # use a subquery to filter references that have any of the requested tags
            # without limiting the outer LEFT JOIN used for collecting all tags
            where_clauses.append(
                f"r.id IN (SELECT rt.reference_id FROM reference_taggins rt "
                f"JOIN tags t2 ON t2.id = rt.tag_id WHERE t2.name IN :{param_name})"
            )
            params[param_name] = tuple(values)
        elif filter_type == "keyword":
            search_word = values[1]
            search_word = search_word.strip()
            search_field = values[0]
            returned_ids = set()

            if search_field == "any":
                returned_ids.update(id_search_any_field(search_word))
                returned_ids.update(id_search_keys_partial(search_word))
            elif search_field == "key":
                returned_ids.update(id_search_keys_partial(search_word))
            else:
                returned_ids.update(id_search_specific_field(search_field, search_word))

            where_clauses.append(f"r.id IN :{param_name}")
            if not returned_ids:
                params[param_name] = (-1,)
            else:
                params[param_name] = tuple(returned_ids)

    if where_clauses:
        sql_parts.append("WHERE " + " AND ".join(where_clauses))

    sql_parts.append("GROUP BY r.id")
    sql_parts.append(f"ORDER BY {order_sql}")

    sql = text(" ".join(sql_parts))
    rows = db.session.execute(sql, params).fetchall()
    return [row_to_reference(row) for row in rows]


def delete_reference(reference_key: str):
    sql = text("DELETE FROM reference_table WHERE reference_key = :reference_key")
    db.session.execute(sql, { "reference_key": reference_key })
    db.session.commit()

def delete_references(reference_keys: list[str]):
    if not reference_keys:
        return

    placeholders = ", ".join(f":k{i}" for i in range(len(reference_keys)))
    params = {f"k{i}": reference_keys[i] for i in range(len(reference_keys))}
    sql = text(f"DELETE FROM reference_table WHERE reference_key IN ({placeholders})")
    db.session.execute(sql, params)
    db.session.commit()

def update_reference(reference_type: str, old_reference_key: str, new_reference_key: str,
                     reference_content: dict, tags: list[str], comment: str = ''):
    reference = get_reference_by_key(old_reference_key)
    if reference is None:
        raise ValueError("Reference not found")

    sql = text("UPDATE reference_table " \
               "SET reference_type = :reference_type, " \
                   "reference_key = :new_reference_key, " \
                   "reference_data = :reference_data, " \
                   "comment = :comment " \
               "WHERE reference_key = :old_reference_key")
    db.session.execute(sql, { "reference_type": reference_type, "old_reference_key": old_reference_key,
                              "reference_data": json.dumps(reference_content),
                              "new_reference_key": new_reference_key,
                              "comment": comment})
    delete_tags_from_reference(reference.id, commit=False)
    add_tags_to_reference(reference.id, tags, commit=False)
    db.session.commit()

# Function for some story tests to skip frontend to add a reference.
def add_ref_for_storytests():
    story_reference_type = "book"
    story_reference_key = "ROBSTORY01"
    story_comment = ""
    story_reference_data = {
        "author": "Rob Bot",
        "title": "Story Book 1",
        "publisher": "Robot Publishing",
        "year": "2000"
    }
    create_reference(story_reference_type, story_reference_key, story_reference_data, story_comment)
