from django.db.models import CASCADE, SET_NULL, ForeignKey, Model

from telegram_users.models.telegram_users import TelegramUsersModel


class UserReferralsModel(Model):
    """Users referrals model."""

    telegram = ForeignKey(TelegramUsersModel, on_delete=CASCADE)
    friend_telegram = ForeignKey(
        TelegramUsersModel,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="friend_telegram_id",
    )

    def __str__(self) -> str:
        return f"{self.telegram.user_name} - пригласил {self.friend_telegram.user_name}"

    class Meta:
        verbose_name = "User referrals"
        verbose_name_plural = "Users referrals"
        db_table = "users_referrals"
