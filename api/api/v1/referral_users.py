from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from dto.models import ReferralUserModelDTO
from dto.requests.referral_users import CreateReferralUserDTO
from dto.responses import OneResponseDTO
from functions import api_key_required
from models import Users, UsersReferrals


version_1_referral_router = APIRouter(
    prefix='/api/v1/referrals',
    tags=['Referrals'],
    dependencies=[Depends(api_key_required)],
    responses={status.HTTP_401_UNAUTHORIZED: {'description': 'Invalid API Key'}},
)


@version_1_referral_router.post(
    path='/',
    response_model=OneResponseDTO[ReferralUserModelDTO],
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'Telegram user not found.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Referral already exist.'},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_referral_user(request: CreateReferralUserDTO, db: Session = Depends(get_db)):
    """Create referral user."""

    telegram_id = request.telegram_user_id
    friend_telegram_id = request.friend_telegram_id

    telegram_user = db.query(Users).filter(Users.telegram_id == telegram_id).first()
    if not telegram_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Telegram user not found.')

    friend_telegram_user = db.query(Users).filter(Users.telegram_id == friend_telegram_id).first()
    if not friend_telegram_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Friend telegram user not found.')
    
    if db.query(UsersReferrals).filter(UsersReferrals.friend_telegram_id == friend_telegram_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Referral already exist.')

    new_referral = UsersReferrals(telegram_id=telegram_id, friend_telegram_id=friend_telegram_id)
    db.add(new_referral)
    db.commit()

    friends = db.query(Users).filter(Users.telegram_id == telegram_id).first()

    referrals = friends.__dict__
    referrals['friends'] = [referral.friend.telegram_id for referral in friends.referrals]

    return OneResponseDTO(detail=ReferralUserModelDTO(**referrals))
