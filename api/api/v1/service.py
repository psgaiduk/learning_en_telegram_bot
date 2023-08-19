from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from functions import api_key_required
from models import LevelsEn, LevelsEnDTO


version_1_service_router = APIRouter(
    prefix='/api/v1/service',
    tags=['Service'],
    dependencies=[Depends(api_key_required)]
)


@version_1_service_router.get('/english_levels/')
async def get_english_levels(db: Session = Depends(get_db)) -> list[LevelsEnDTO]:
    """Get all english levels."""
    english_levels = db.query(LevelsEn).all()
    return [LevelsEnDTO(**level.__dict__) for level in english_levels]
