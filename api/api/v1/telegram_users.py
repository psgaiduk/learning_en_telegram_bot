from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from database import get_db
from dto.models import TelegramUserDTO, UpdateTelegramUserDTO
from functions import api_key_required
from models import Users


version_1_telegram_user_router = APIRouter(
    prefix='/api/v1/telegram_user',
    tags=['Users'],
    dependencies=[Depends(api_key_required)]
)


async def get_user_by_telegram_id(telegram_id: int, db: Session = Depends(get_db)) -> Users:
    """Get user by telegram id."""

    telegram_user = (
        db.query(Users)
        .options(joinedload(Users.main_language))
        .filter(Users.telegram_id == telegram_id)
        .first()
    )

    if not telegram_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return telegram_user


async def get_telegram_user_dto(telegram_user: Users) -> TelegramUserDTO:
    """Get telegram user DTO."""

    telegram_user_dict = telegram_user.__dict__
    telegram_user_dict["main_language"] = telegram_user.main_language.__dict__
    telegram_user_dict["level_en"] = telegram_user.level_en.__dict__

    return TelegramUserDTO(**telegram_user_dict)


@version_1_telegram_user_router.post('/', response_model=TelegramUserDTO)
async def create_user(user: TelegramUserDTO, db: Session = Depends(get_db)):

    new_user = Users(
        telegram_id=user.telegram_id,
        level_en_id=user.level_en_id,
        main_language_id=user.main_language_id,
        user_name=user.user_name,
        experience=user.experience,
        hero_level_id=user.hero_level_id,
        previous_stage=user.previous_stage,
        stage=user.stage
    )
    db.add(new_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        db.close()
    return user


@version_1_telegram_user_router.get('/{telegram_id}/')
async def get_user(telegram_id: int, db: Session = Depends(get_db)) -> TelegramUserDTO:

    telegram_user = await get_user_by_telegram_id(telegram_id, db)
    return await get_telegram_user_dto(telegram_user)


@version_1_telegram_user_router.patch('/{telegram_id}/')
async def update_user(telegram_id: int, updated_data: UpdateTelegramUserDTO, db: Session = Depends(get_db)):

    existing_user = await get_user_by_telegram_id(telegram_id, db)

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    for field, value in updated_data.dict(exclude_unset=True).items():
        setattr(existing_user, field, value)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return await get_telegram_user_dto(existing_user)
