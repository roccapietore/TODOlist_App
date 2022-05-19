from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from goals.models import GoalComment
from goals.permissions import CommentPermissions
from goals.serializers import CommentCreateSerializer, CommentSerializer


class CommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [CommentPermissions]
    serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [CommentPermissions]
    serializer_class = CommentSerializer
    filter_backends = [
        OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["goal"]
    ordering = ["-id"]

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [CommentPermissions]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)
