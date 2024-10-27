from datetime import datetime, timezone

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.orm import Session, joinedload

from dto.models import UserStatsModelDTO
from models import Users, UsersWordsHistory


class GetReadUserStatsService:
    """Get stats for today for user."""

    def __init__(self, telegram_id: int, db: Session) -> None:
        self.telegram_id = telegram_id
        self.db = db
        self.user_stats = UserStatsModelDTO(
            count_of_new_words=0,
            count_of_words=0,
            time_to_next_word=0,
        )

    async def work(self) -> str:
        await self._get_user()
        await self._get_word_history()
        await self._get_time_for_repeat_word()
        return self.user_stats

    async def _get_user(self):
        self.user = (
            self.db.query(Users)
            .filter(Users.telegram_id == self.telegram_id)
            .options(joinedload(Users.hero_level))
            .first()
        )
        logger.debug(f"Get users by id {self.telegram_id}")
        logger.debug(f"User: {self.user}")

        if not self.user:
            logger.debug("User not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    async def _get_word_history(self) -> None:

        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        today_words = (
            self.db.query(UsersWordsHistory)
            .filter(UsersWordsHistory.telegram_user_id == self.telegram_id, UsersWordsHistory.updated_at >= today_start)
            .all()
        )

        if not today_words:
            return

        for word in today_words:
            if word.created_at.tzinfo is None:
                word.created_at = word.created_at.replace(tzinfo=timezone.utc)
            self.user_stats.count_of_words += 1
            if word.created_at >= today_start:
                self.user_stats.count_of_new_words += 1

    async def _get_time_for_repeat_word(self) -> None:
        next_word = (
            self.db.query(UsersWordsHistory)
            .filter(
                UsersWordsHistory.telegram_user_id == self.telegram_id,
            )
            .order_by(UsersWordsHistory.repeat_datetime)
            .first()
        )

        if not next_word:
            return

        now = datetime.now(timezone.utc)
        logger.debug(f'now time = {now}, repeat_time = {next_word.repeat_datetime}')
        if next_word.repeat_datetime.tzinfo is None:
            logger.debug('not timezone add it')
            next_word.repeat_datetime = next_word.repeat_datetime.replace(tzinfo=timezone.utc)
        logger.debug(f'now time = {now}, repeat_time = {next_word.repeat_datetime}')
        time_to_next_word = (next_word.repeat_datetime - now).total_seconds() / 60
        self.user_stats.time_to_next_word = max(time_to_next_word, 0)
