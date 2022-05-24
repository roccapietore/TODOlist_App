import os
from django.core.management.base import BaseCommand
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from todolist import settings


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    @staticmethod
    def _generate_code() -> str:
        return os.urandom(12).hex()

    def handle_user_without_verifications(self, message: Message, tg_user: TgUser):
        code: str = self._generate_code()
        tg_user.verification_code = code
        tg_user.save(update_fields=['verification_code'])

        self.tg_client.send_message(chat_id=message.chat.id, text=f'[verification code] {code}')

    def handle_message(self, message: Message):
        tg_user, created = TgUser.objects.get_or_create(
            chat_id=message.chat.id,
            defaults={'username': message.from_.username}
        )
        if created:
            self.tg_client.send_message(chat_id=message.chat.id, text='[Hello]')
        elif not tg_user.user:
            self.handle_user_without_verifications(message=message, tg_user=tg_user)

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
                self.tg_client.send_message(chat_id=item.message.chat.id, text=item.message.text)

