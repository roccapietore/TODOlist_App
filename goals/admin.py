from django.contrib import admin
from django.db.models import Count
from goals.models import GoalCategory, Goal, GoalComment, Board


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


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "priority", "deadline_date")
    search_fields = ("title", "user")


@admin.register(GoalComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
    search_fields = ("text",)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "is_deleted")
    search_fields = ("title",)
    list_filter = ("is_deleted",)

