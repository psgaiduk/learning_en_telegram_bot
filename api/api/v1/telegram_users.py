from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from database import create_commit, get_db
from dto.models import TelegramUserDTO
from dto.requests.telegram_users import CreateTelegramUserDTO, UpdateTelegramUserDTO
from dto.responses import OneResponseDTO
from functions import api_key_required, patch_data
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
        .options(joinedload(Users.main_language), joinedload(Users.level_en), joinedload(Users.hero_level))
        .filter(Users.telegram_id == telegram_id)
        .first()
    )

    if not telegram_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return telegram_user


async def get_telegram_user_dto(telegram_user: Users) -> OneResponseDTO[TelegramUserDTO]:
    """Get telegram user DTO."""

    telegram_user_dict = telegram_user.__dict__
    telegram_user_dict['main_language'] = telegram_user.main_language.__dict__
    if telegram_user.level_en:
        telegram_user_dict['level_en'] = telegram_user.level_en.__dict__
    else:
        telegram_user_dict['level_en'] = None
    telegram_user_dict['hero_level'] = telegram_user.hero_level.__dict__

    return OneResponseDTO(detail=TelegramUserDTO(**telegram_user_dict))


@version_1_telegram_user_router.post(
    path='/',
    response_model=OneResponseDTO[TelegramUserDTO],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(request: CreateTelegramUserDTO, db: Session = Depends(get_db)):
    """Create telegram user."""
    print('here create_user')
    new_user = Users(
        telegram_id=request.telegram_id,
        level_en_id=request.level_en_id,
        main_language_id=request.main_language_id,
        user_name=request.user_name,
        experience=request.experience,
        hero_level_id=request.hero_level_id,
        previous_stage=request.previous_stage,
        stage=request.stage
    )
    db.add(new_user)
    
    print(new_user, 'new_user')

    await create_commit(db)

    return await get_user(request.telegram_id, db)


@version_1_telegram_user_router.get(
    path='/{telegram_id}/',
    response_model=OneResponseDTO[TelegramUserDTO],
)
async def get_user(telegram_id: int, db: Session = Depends(get_db)):
    """Get telegram user."""

    telegram_user = await get_user_by_telegram_id(telegram_id, db)
    print('here get_user', telegram_user)
    return await get_telegram_user_dto(telegram_user)


@version_1_telegram_user_router.patch(
    path='/{telegram_id}/',
    responses={status.HTTP_404_NOT_FOUND: {'description': 'User not found.'}},
    response_model=OneResponseDTO[TelegramUserDTO],
)
async def update_user(
        telegram_id: int,
        request: UpdateTelegramUserDTO,
        db: Session = Depends(get_db),
):
    """Update telegram user."""

    existing_user = await get_user_by_telegram_id(telegram_id, db)

    existing_user = patch_data(object_from_db=existing_user, request=request)

    await create_commit(db)

    return await get_telegram_user_dto(existing_user)
