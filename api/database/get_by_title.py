from typing import Optional

from sqlalchemy.orm import Session


def get_id_by_title(db: Session, model, title: str) -> Optional[int]:
    """
    Get item id by title.

    :param db: session.
    :param model: model where we find id by title.
    :param title: text title.
    :return: id or None.
    """
    record = db.query(model).filter_by(title=title).first()
    if record:
        return record.id

    return
