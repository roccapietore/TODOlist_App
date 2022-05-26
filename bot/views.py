from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TGUserSerializer
from bot.tg.client import TgClient
from todolist import settings


class VerificationView(GenericAPIView):
    model = TgUser
    serializer_class = TGUserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        s: TGUserSerializer = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)

        tg_user: TgUser = s.validated_data['tg_user']
        tg_user.user = self.request.user
        print(self.request.user)
        tg_user.save(update_fields=['user'])

        instance: TGUserSerializer = self.get_serializer(tg_user)
        TgClient(settings.BOT_TOKEN).send_message(tg_user.telegram_chat_id, 'verification has completed')

        return Response(instance.data)

