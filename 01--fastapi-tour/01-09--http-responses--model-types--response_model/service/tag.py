from typing import Dict

from model.tag import Tag

db: Dict[str, Tag] = {}
# Note:
# `reload=True` restarts the process when files changes.
# In-memory data like `db = {}` is lost after restart.

def create_tag(tag_obj: Tag) -> None:
    db[tag_obj.tag] = tag_obj


def get_tag(tag: str) -> Tag | None:
    return db.get(tag)
