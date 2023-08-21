from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from dto import TelegramUserDTO
from functions import api_key_required
from models import Users


version_1_telegram_user_router = APIRouter(
    prefix='/api/v1/telegram_user',
    tags=['Users'],
    dependencies=[Depends(api_key_required)]
)


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
