from config import db
from sqlalchemy import text

from entities.todo import Citation

def get_todos():
    result = db.session.execute(text("SELECT id, citation_key, citation_type, citation_data FROM citations"))
    todos = result.fetchall()
    return [Citation(todo[0], todo[1], todo[2], todo[3]) for todo in todos] 

def set_done(todo_id):
    pass
    #sql = text("UPDATE todos SET done = TRUE WHERE id = :id")
    #db.session.execute(sql, { "id": todo_id })
    #db.session.commit()

def create_todo(citation_type, citation_key, citation_data):
    sql = text("INSERT INTO citations (citation_type, citation_key, citation_data) VALUES (:citation_type, :citation_key, :citation_data )")
    db.session.execute(sql, { "citation_type": citation_type, "citation_key": citation_key, "citation_data": citation_data})
    db.session.commit()
