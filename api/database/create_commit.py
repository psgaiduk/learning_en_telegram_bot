from fastapi import HTTPException, status
from sqlalchemy.orm import Session


async def create_commit(db: Session) -> None:
    """
    Create a database commit.

    :params db: The session object representing the database connection.

    :raises: HTTPException: If there is an error when committing the changes to the database.
    """

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
