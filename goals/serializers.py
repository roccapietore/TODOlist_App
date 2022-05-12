from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, GoalComment


class CategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")
        return value


class GoalCreateSerializer(GoalSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class CommentCreateSerializer(ModelSerializer):

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def validate_category(self, value):
        if value.uset != self.context["request"].user:
            raise serializers.ValidationError("You are not the owner")
        return value


class CommentSerializer(CommentCreateSerializer):
    user = UserSerializer(read_only=True, source='goal.user')


