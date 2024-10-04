from django.contrib import admin

from telegram_users.models import UserReferralsModel


@admin.register(UserReferralsModel)
class UserReferralsAdmin(admin.ModelAdmin):
    """User referrals admin."""

    list_display = ("__str__",)
    search_fields = ("telegram_id__telegram_id",)
