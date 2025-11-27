import json
from sqlalchemy import text
#from entities.reference import Reference, ReferenceType
from config import db


def get_tags_with_counts():
    """Return a list of tags with their reference counts ordered by count desc.

    Each item is a dict: { 'name': str, 'count': int }
    """
    sql = text(
        "SELECT t.name, COUNT(rt.reference_id) as cnt "
        "FROM tags t "
        "LEFT JOIN reference_taggins rt ON rt.tag_id = t.id "
        "GROUP BY t.id "
        "ORDER BY cnt DESC, t.name ASC"
    )
    rows = db.session.execute(sql).fetchall()
    return [{ 'name': row[0], 'count': int(row[1]) } for row in rows]
    
def get_tags_by_reference(reference_id: int):
    sql = text(
        "SELECT t.name "
        "FROM tags t "
        "LEFT JOIN reference_taggins rt ON rt.tag_id = t.id "
        "WHERE rt.reference_id = :reference_id"
    )
    tags = db.session.execute(sql, {"reference_id": reference_id}).fetchall()
    return [tag for tag in tags]
    
def update_tags():
    pass
