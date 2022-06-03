from django.db import transaction
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from goals.models import Board, Goal
from goals.permissions import BoardPermissions
from goals.serializers import BoardSerializer, BoardCreateSerializer, BoardListSerializer


class BoardCreateView(CreateAPIView):
    """"
    Создание досок доступно зарегистрированным пользователям.
    """
    model = Board
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    """
    Просмотр досок доступен всем зарегистрированным пользователям.
    Редактирование, удаление досок доступно создателям доски.
    """
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user.id, is_deleted=False)

    def perform_destroy(self, instance: Board):
        """При удалении доски помечаем ее как is_deleted, «удаляем» категории, обновляем статус целей"""
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)
        return instance


class BoardListView(ListAPIView):
    """
    Просмотр списка досок доступен всем зарегистрированным пользователям.
    """
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardListSerializer
    filter_backends = [OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user.id, is_deleted=False)


