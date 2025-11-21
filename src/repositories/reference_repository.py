import json
from sqlalchemy import text
from entities.reference import Reference, ReferenceType
from config import db

def get_references():
    sql = text("SELECT id, reference_key, reference_type, reference_data FROM reference_table")
    rows = db.session.execute(sql).fetchall()
    return [
        Reference(row[0], row[1], ReferenceType(row[2]), row[3])
        for row in rows
    ]

def create_reference(reference_type, reference_key: str, reference_data: str):
    sql = text("INSERT INTO reference_table (reference_type, reference_key, reference_data)" \
                "VALUES (:reference_type, :reference_key, :reference_data )")
    db.session.execute(sql, { "reference_type": reference_type, "reference_key": reference_key,
                             "reference_data": json.dumps(reference_data)})
    db.session.commit()

def get_reference_by_key(key: str):
    sql = text(
        "SELECT id, reference_key, reference_type, reference_data "
        "FROM reference_table WHERE reference_key = :key"
    )
    row = db.session.execute(sql, {"key": key}).fetchone()
    if row is None:
        return None
    return Reference(row[0], row[1], ReferenceType(row[2]), row[3])

def delete_reference(reference_key: str):
    sql = text("DELETE FROM reference_table WHERE reference_key = :reference_key")
    db.session.execute(sql, { "reference_key": reference_key })
    db.session.commit()
