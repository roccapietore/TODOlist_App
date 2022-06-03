from django.db import transaction
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from goals.models import GoalCategory, Goal
from goals.permissions import CategoryPermissions
from goals.serializers import CategoryCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    """"
    Создание категории доступно создателю доски и редактору.
    """
    model = GoalCategory
    permission_classes = [CategoryPermissions]
    serializer_class = CategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """"
    Просмотр списка категорий доступен всем зарегистрированным пользователям.
    """
    model = GoalCategory
    permission_classes = [CategoryPermissions]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_fields = ["board"]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """
    Просмотр категорий доступен зарегистрированным пользователям.
    Редактирование, удаление категорий доступно создателю доски и редактору.
    """
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [CategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        """Обновление поля is_deleted. Удаление категории с доски"""
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
        return instance

