from fastapi import APIRouter, Depends

from functions import api_key_required


version_1_telegram_user_router = APIRouter(
    prefix='/api/v1/telegram_user/',
    tags=['Users'],
    dependencies=[Depends(api_key_required)]
)
