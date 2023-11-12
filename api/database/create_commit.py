from fastapi import HTTPException, status
from sqlalchemy.orm import Session


async def create_commit(db: Session):
    """Create and commit user."""

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
