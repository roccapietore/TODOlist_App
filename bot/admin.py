from django.contrib import admin
from bot.models import TgUser


@admin.register(TgUser)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("telegram_chat_id", "username", "user")
    readonly_fields = ('verification_code', )



