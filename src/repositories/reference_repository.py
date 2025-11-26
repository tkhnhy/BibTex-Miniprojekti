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

def create_reference(reference_type: str, reference_key: str, reference_content: dict, comment: str = ''):
    sql = text("INSERT INTO reference_table (reference_type, reference_key, reference_data, comment)" \
                "VALUES (:reference_type, :reference_key, :reference_data, :comment)")
    db.session.execute(sql, { "reference_type": reference_type, "reference_key": reference_key,
                             "reference_data": json.dumps(reference_content), "comment": comment})
    db.session.commit()

def get_reference_by_key(key: str):
    sql = text(
        "SELECT id, reference_key, reference_type, reference_data, comment "
        "FROM reference_table WHERE reference_key = :key"
    )
    row = db.session.execute(sql, {"key": key}).fetchone()
    if row is None:
        return None
    return Reference(row[0], row[1], ReferenceType(row[2]), row[3], comment=row[4])

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
    story_comment = str("")
    story_reference_data = {
    "author": "Rob Bot",
    "title": "Story Book 1",
    "publisher": "Robot Publishing",
    "year": "2000"
    }
    sql = text("INSERT INTO reference_table (reference_type, reference_key, reference_data, comment)" \
                "VALUES (:reference_type, :reference_key, :reference_data, :comment)")
    db.session.execute(sql, { "reference_type": story_reference_type, "reference_key": story_reference_key,
                             "reference_data": json.dumps(story_reference_data), "comment": story_comment})
    db.session.commit()
