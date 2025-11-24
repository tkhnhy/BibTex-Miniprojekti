import json
from sqlalchemy import text
from entities.reference import Reference, ReferenceType
from config import db

def get_references():
    sql = text("SELECT id, reference_key, reference_type, reference_data, comment FROM reference_table")
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

def update_reference(reference_type: str, old_reference_key: str, new_reference_key: str, reference_content: dict):
    sql = text("UPDATE reference_table " \
               "SET reference_type = :reference_type, " \
                   "reference_key = :new_reference_key, " \
                   "reference_data = :reference_data " \
               "WHERE reference_key = :old_reference_key")
    db.session.execute(sql, { "reference_type": reference_type, "old_reference_key": old_reference_key,
                              "reference_data": json.dumps(reference_content),
                              "new_reference_key": new_reference_key})
    db.session.commit()
