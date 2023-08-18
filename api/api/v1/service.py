from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from functions import api_key_required
from models import LevelsEn


version_1_service_router = APIRouter(
    prefix='/api/v1/service',
    tags=['Service'],
    dependencies=[Depends(api_key_required)]
)


@version_1_service_router.get('/english_levels/')
async def create_user(db: Session = Depends(get_db)):
    """
    Get all english levels.

    :param db: Session
    :return:
    """
    english_levels = db.query(LevelsEn).all()
    return english_levels
