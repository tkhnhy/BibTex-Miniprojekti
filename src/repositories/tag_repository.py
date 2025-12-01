from sqlalchemy import text
from config import db
from entities.tag import Tag

def get_tags_with_counts()-> list[tuple[Tag, int]]:
    """Return a list of tags with their reference counts ordered by count desc."""
    sql = text(
        "SELECT t.name, COUNT(rt.reference_id) as cnt "
        "FROM tags t "
        "LEFT JOIN reference_taggins rt ON rt.tag_id = t.id "
        "GROUP BY t.id "
        "ORDER BY cnt DESC, t.name ASC"
    )
    rows = db.session.execute(sql).fetchall()
    return [(Tag(name=row[0]), int(row[1])) for row in rows]

def get_reference_tags(reference_id: int):
    sql = text(
        "SELECT t.name "
        "FROM tags t "
        "JOIN reference_taggins rt ON rt.tag_id = t.id "
        "WHERE rt.reference_id = :reference_id "
        "ORDER BY t.name"
    )
    rows = db.session.execute(sql, {"reference_id": reference_id}).fetchall()
    return [Tag(name=row[0]) for row in rows]

def update_tags():
    pass
