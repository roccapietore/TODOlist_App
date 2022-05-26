from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from bot.models import TgUser


class TGUserSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(write_only=True)
    tg_id = serializers.SlugField(read_only=True)

    class Meta:
        model = TgUser
        fields = (
            "username",
            "user_id",
            "verification_code",
            'tg_id',
        )
        read_only_fields = ('tg_id', "username", "user_id", )

    def validate(self, attrs):
        verification_code = attrs.get('verification_code')
        tg_user = TgUser.objects.filter(verification_code=verification_code).first()

        if not tg_user:
            raise ValidationError({"verification error"})
        attrs['tg_user'] = tg_user

        return attrs

