from django.db import models
from core.models import User


class TgUser(models.Model):
    telegram_chat_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True, default=None)
    user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.PROTECT)
    verification_code = models.CharField(max_length=55, null=True, blank=True, default=None)

    class Meta:
        verbose_name = "TG Пользователь"
        verbose_name_plural = "TG Пользователи"

    def __str__(self):
        if self.username:
            return self.username
        elif self.user and self.user.username:
            return self.user.username
        else:
            return super().__str__()





