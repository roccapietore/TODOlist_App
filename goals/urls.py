from django.urls import path
from goals.views import categories, goals, comments, boards


urlpatterns = [
    path("goal_category/create", categories.GoalCategoryCreateView.as_view()),
    path("goal_category/list", categories.GoalCategoryListView.as_view()),
    path("goal_category/<pk>", categories.GoalCategoryView.as_view()),

    path("goal/create", goals.GoalCreateView.as_view()),
    path("goal/list", goals.GoalListView.as_view()),
    path("goal/<pk>", goals.GoalView.as_view()),

    path("goal_comment/create", comments.CommentCreateView.as_view()),
    path("goal_comment/list", comments.CommentListView.as_view()),
    path("goal_comment/<pk>", comments.CommentView.as_view()),

    path("board/create", boards.BoardCreateView.as_view()),
    path("board/list", boards.BoardListView.as_view()),
    path("board/<pk>", boards.BoardView.as_view()),
]


