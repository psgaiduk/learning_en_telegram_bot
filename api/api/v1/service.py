from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from dto.models import LevelsEnModelDTO
from functions import api_key_required
from models import LevelsEn, MainLanguages, MainLanguagesModelDTO, HeroLevels, HeroLevelsModelDTO


version_1_service_router = APIRouter(
    prefix='/api/v1/service',
    tags=['Service'],
    dependencies=[Depends(api_key_required)],
    responses={status.HTTP_401_UNAUTHORIZED: {'description': 'Invalid API Key'}},
)


@version_1_service_router.get('/english_levels/')
async def get_english_levels(db: Session = Depends(get_db)) -> list[LevelsEnModelDTO]:
    """Get all english levels."""
    english_levels = db.query(LevelsEn).all()
    return [LevelsEnModelDTO(**level.__dict__) for level in english_levels]


@version_1_service_router.get('/languages/')
async def get_languages(db: Session = Depends(get_db)) -> list[MainLanguagesModelDTO]:
    """Get all languages."""
    languages = db.query(MainLanguages).all()
    return [MainLanguagesModelDTO(**level.__dict__) for level in languages]


@version_1_service_router.get('/hero_levels/')
async def get_hero_levels(db: Session = Depends(get_db)) -> list[HeroLevelsModelDTO]:
    """Get all hero levels."""
    hero_levels = db.query(HeroLevels).all()
    return [HeroLevelsModelDTO(**level.__dict__) for level in hero_levels]


@version_1_service_router.get(
    '/hero_levels/{number}/',
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'Hero level not found'},
    },
)
async def get_hero_levels_by_number(number: int, db: Session = Depends(get_db)) -> HeroLevelsModelDTO:
    """Get all hero levels."""
    hero_levels = db.query(HeroLevels).filter(HeroLevels.order == number).first()
    if not hero_levels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hero level not found')
    return HeroLevelsModelDTO(**hero_levels.__dict__)
