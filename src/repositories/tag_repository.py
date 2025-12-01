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

def add_tags_to_reference(reference_id: int, tag_names: list[str], *, commit: bool = True):
    for tag_name in tag_names:
        # Check if the tag exists
        sql_select = text("SELECT id FROM tags WHERE name = :name")
        result = db.session.execute(sql_select, {"name": tag_name}).fetchone()
        if result:
            tag_id = result[0]
        else:
            # Insert new tag if not found
            sql_insert_tag = text("INSERT INTO tags (name) VALUES (:name) RETURNING id")
            tag_id = db.session.execute(sql_insert_tag, {"name": tag_name}).fetchone()[0]

        # Add link between reference and tag
        sql_insert_link = text(
            "INSERT INTO reference_taggins (reference_id, tag_id) "
            "VALUES (:reference_id, :tag_id) "
            "ON CONFLICT DO NOTHING" # just skip existing links
        )
        db.session.execute(sql_insert_link, {"reference_id": reference_id, "tag_id": tag_id})
    if commit:
        db.session.commit()

def delete_tags_from_reference(reference_id: int, *, commit: bool = True):
    sql = text("DELETE FROM reference_taggins WHERE reference_id = :reference_id")
    db.session.execute(sql, {"reference_id": reference_id})
    if commit:
        db.session.commit()

def update_tags():
    pass
