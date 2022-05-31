from django.urls import path
from goals.views import categories, goals, comments, boards


urlpatterns = [
    path("goal_category/create", categories.GoalCategoryCreateView.as_view(), name='category_create'),
    path("goal_category/list", categories.GoalCategoryListView.as_view(), name='category_list'),
    path("goal_category/<pk>", categories.GoalCategoryView.as_view(), name='category_id'),

    path("goal/create", goals.GoalCreateView.as_view(), name='goal_create'),
    path("goal/list", goals.GoalListView.as_view(), name='goal_list'),
    path("goal/<pk>", goals.GoalView.as_view(), name='goal_id'),

    path("goal_comment/create", comments.CommentCreateView.as_view(), name='comment_create'),
    path("goal_comment/list", comments.CommentListView.as_view(), name='comment_list'),
    path("goal_comment/<pk>", comments.CommentView.as_view(), name='comment_id'),

    path("board/create", boards.BoardCreateView.as_view(), name='board_create'),
    path("board/list", boards.BoardListView.as_view(), name='board_list'),
    path("board/<pk>", boards.BoardView.as_view(), name='board_id'),
]


