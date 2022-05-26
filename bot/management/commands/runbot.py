import os
from enum import unique, auto, Enum
from typing import Optional

from django.core.management.base import BaseCommand
from emoji import emojize
from pydantic import BaseModel
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory
from todolist import settings


class NewGoal(BaseModel):
    category_id: Optional[int] = None
    goal_title: Optional[str] = None

    def complete(self):
        return None not in [self.category_id, self.goal_title]


@unique
class StateEnum(Enum):
    CREATE_CATEGORY_STATE = auto()
    CHOSEN_CATEGORY = auto()


class FSMData(BaseModel):
    state: StateEnum
    goal: NewGoal


FSM_states: dict[int, FSMData] = dict()


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

    def handle_verified_user(self, message: Message, tg_user: TgUser):
        if message.text == '/goals':
            self.handle_goals_list(message=message, tg_user=tg_user)

        elif message.text == '/create':
            self.handle_category_list(message=message, tg_user=tg_user)
            FSM_states[tg_user.telegram_chat_id] = FSMData(state=StateEnum.CREATE_CATEGORY_STATE, goal=NewGoal())

        elif message.text == '/cancel' and tg_user.telegram_chat_id in FSM_states:
            self.tg_client.send_message(message.chat.id, text=f"[operation has canceled]")
            FSM_states.pop(tg_user.telegram_chat_id)

        elif tg_user.telegram_chat_id in FSM_states:
            state: StateEnum = FSM_states[tg_user.telegram_chat_id].state

            if state == StateEnum.CREATE_CATEGORY_STATE:
                self.handle_save_selected_category(message=message, tg_user=tg_user)

            elif state == StateEnum.CHOSEN_CATEGORY:
                self.save_new_goal(message=message, tg_user=tg_user)

        elif message.text.startswith('/'):
            self.tg_client.send_message(message.chat.id, text=f"[unknown command]")

    def handle_save_selected_category(self, message: Message, tg_user: TgUser):
        if message.text.isdigit():
            cat_id = int(message.text)
            if GoalCategory.objects.filter(
                    board__participants__user_id=tg_user.user_id,
                    is_deleted=False,
                    id=cat_id).count():
                FSM_states[tg_user.telegram_chat_id].goal.category_id = cat_id
                self.tg_client.send_message(message.chat.id, text='[set the title]')
                FSM_states[tg_user.telegram_chat_id].state = StateEnum.CHOSEN_CATEGORY
                return

        self.tg_client.send_message(message.chat.id, text='[invalid category id]')

    def save_new_goal(self, message: Message, tg_user: TgUser):
        goal: NewGoal = FSM_states[tg_user.telegram_chat_id].goal
        goal.goal_title = message.text
        if goal.complete():
            Goal.objects.create(
                title=goal.goal_title,
                category_id=goal.category_id,
                user_id=tg_user.user_id
            )
            self.tg_client.send_message(message.chat.id, text='[new goal has created]')
        else:
            self.tg_client.send_message(message.chat.id, text='[error]')

        FSM_states.pop(tg_user.telegram_chat_id, None)

    def handle_goals_list(self, message: Message, tg_user: TgUser):
        goals_list: list[str] = \
            [f"{goal.title} {emojize(':slightly_smiling_face:')} {goal.description}"
             for goal in Goal.objects.filter(user_id=tg_user.user_id)]

        self.tg_client.send_message(message.chat.id, '\n'.join(goals_list) or '[goals weren`t found]')

    def handle_category_list(self, message: Message, tg_user: TgUser):
        category_list: list[str] = \
            [f"{category.id} - {category.title}"
             for category in GoalCategory.objects.filter(
                board__participants__user_id=tg_user.user_id,
                is_deleted=False)]

        if category_list:
            self.tg_client.send_message(message.chat.id, text='Select category\n{}'.format('\n'.join(category_list)))
        else:
            self.tg_client.send_message(message.chat.id, '[category wasn`t found]')

    def handle_message(self, message: Message):
        tg_user, created = TgUser.objects.get_or_create(
            telegram_chat_id=message.chat.id,
            defaults={'username': message.from_.username}
        )
        if created:
            self.tg_client.send_message(chat_id=message.chat.id, text='[Hello]')
        elif not tg_user.user:
            self.handle_user_without_verifications(message=message, tg_user=tg_user)
        else:
            self.handle_verified_user(message=message, tg_user=tg_user)

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)
