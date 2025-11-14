from config import db
from sqlalchemy import text
import json

from entities.reference import Reference

def get_references():
    result = db.session.execute(text("SELECT id, reference_key, reference_type, reference_data FROM reference_table"))
    references = result.fetchall()
    return [Reference(reference[0], reference[1], reference[2], reference[3]) for reference in references] 

def set_done(reference_id):
    pass
    #sql = text("UPDATE todos SET done = TRUE WHERE id = :id")
    #db.session.execute(sql, { "id": todo_id })
    #db.session.commit()

def create_reference(reference_type, reference_key, reference_data):
    sql = text("INSERT INTO reference_table (reference_type, reference_key, reference_data) VALUES (:reference_type, :reference_key, :reference_data )")
    db.session.execute(sql, { "reference_type": reference_type, "reference_key": reference_key, "reference_data": json.dumps(reference_data)})
    db.session.commit()

def db_delete_reference(reference_key):
    sql = text("DELETE FROM reference_table WHERE reference_key = :reference_key")
    db.session.execute(sql, { "reference_key": reference_key })
    db.session.commit()
