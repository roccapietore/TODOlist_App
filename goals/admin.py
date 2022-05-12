from django.contrib import admin
from goals.models import GoalCategory, Goal, GoalComment


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "priority", "deadline_date")
    search_fields = ("title", "user")


@admin.register(GoalComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
    search_fields = ("text",)

