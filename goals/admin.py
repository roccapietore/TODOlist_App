from django.contrib import admin
from django.db.models import Count
from goals.models import GoalCategory, Goal, GoalComment, BoardParticipant, Board


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 0
    show_change_link = True

    def _get_form_for_get_fields(self, request, obj=None):
        return self.get_formset(request, obj, fields=('title', 'status', 'deadline_date')).form

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated", "goals_count")
    search_fields = ("title", "user")
    inlines = (GoalInline, )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_goals_count=Count('goal', distinct=True))
        return queryset

    def goals_count(self, obj):
        return obj._goals_count

    goals_count.short_description = 'Количество целей'


@admin.register(GoalComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
    search_fields = ("text",)


class BoardInline(admin.TabularInline):
    model = BoardParticipant
    extra = 0
    show_change_link = True

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()
        queryset = queryset.exclude(role=BoardParticipant.Role.owner)
        return queryset


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "is_deleted", 'owner', 'participants_count',)
    search_fields = ("title",)
    list_filter = ("is_deleted",)
    inlines = (BoardInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('participants')
        return queryset

    def owner(self, obj):
        return obj.participants.filter(role=BoardParticipant.Role.owner).get().user

    def participants_count(self, obj):
        return obj.participants_count - 1

    owner.short_description = 'Создатель доски'
    participants_count.short_description = 'Количество участников'

