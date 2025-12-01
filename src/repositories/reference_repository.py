import json
from sqlalchemy import text
from entities.reference import Reference, ReferenceType
from config import db

def get_references():
    sql = text("SELECT id, reference_key, reference_type, reference_data, comment" \
                " FROM reference_table ORDER BY id")
    rows = db.session.execute(sql).fetchall()
    return [
        Reference(row[0], row[1], ReferenceType(row[2]), row[3], comment=row[4])
        for row in rows
    ]

def get_references_by_keys(keys: list[str]):
    if not keys:
        return []

    placeholders = ", ".join(f":k{i}" for i in range(len(keys)))
    sql = text(
        "SELECT id, reference_key, reference_type, reference_data, comment "
        f"FROM reference_table WHERE reference_key IN ({placeholders})"
    )
    params = {f"k{i}": keys[i] for i in range(len(keys))}
    rows = db.session.execute(sql, params).fetchall()

    refs = [
        Reference(row[0], row[1], ReferenceType(row[2]), row[3], comment=row[4])
        for row in rows
    ]
    # Preserve order
    ref_map = {r.key: r for r in refs}
    ordered_refs = [ref_map[k] for k in keys if k in ref_map]
    return ordered_refs

def create_reference(reference_type: str, reference_key: str, reference_content: dict, comment: str = ''):
    try:
        sql = text("INSERT INTO reference_table (reference_type, reference_key, reference_data, comment)" \
                    "VALUES (:reference_type, :reference_key, :reference_data, :comment)")
        db.session.execute(sql, { "reference_type": reference_type, "reference_key": reference_key,
                                 "reference_data": json.dumps(reference_content), "comment": comment})
        db.session.commit()
    except Exception as error:
        print("Error when creating reference:", error)

def get_reference_by_key(key: str):
    sql = text(
        "SELECT id, reference_key, reference_type, reference_data, comment "
        "FROM reference_table WHERE reference_key = :key"
    )
    row = db.session.execute(sql, {"key": key}).fetchone()
    if row is None:
        return None
    # print("Fetched reference row:", row)
    return Reference(row[0], row[1], ReferenceType(row[2].lower()), row[3], comment=row[4])

def get_filtered_references(filters):

    sql_parts = [
        "SELECT id, reference_key, reference_type, reference_data, comment",
        "FROM reference_table"
    ]
    where_clauses = []
    params = {}

    # Build WHERE clauses dynamically
    for filter_type, values in filters:
        if not values:
            continue

        param_name = f"{filter_type}_vals"

        if filter_type == "type":
            where_clauses.append(f"reference_type IN :{param_name}")
            params[param_name] = tuple(values)

    if where_clauses:
        sql_parts.append("WHERE " + " AND ".join(where_clauses))

    sql_parts.append("ORDER BY id")

    sql = text(" ".join(sql_parts))

    rows = db.session.execute(sql, params).fetchall()

    # Map each row to a Reference object; duplicates should not occur if query is correct
    return [
        Reference(
            row[0],
            row[1],
            ReferenceType(row[2]),
            row[3],
            comment=row[4]
        )
        for row in rows
    ]
def delete_reference(reference_key: str):
    sql = text("DELETE FROM reference_table WHERE reference_key = :reference_key")
    db.session.execute(sql, { "reference_key": reference_key })
    db.session.commit()

def update_reference(reference_type: str, old_reference_key: str, new_reference_key: str,
                     reference_content: dict, comment: str = ''):
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
