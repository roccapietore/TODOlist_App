from django.db import transaction
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from goals.models import GoalCategory, Goal
from goals.permissions import CategoryPermissions
from goals.serializers import CategoryCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [CategoryPermissions]
    serializer_class = CategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [CategoryPermissions]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filter_fields = ["board"]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [CategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.goals.update(status=Goal.Status.archived)
            instance.save()
        return instance

