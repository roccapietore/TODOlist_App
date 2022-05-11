from django.urls import path
from goals.views import categories, goals


urlpatterns = [
    path("goal_category/create", categories.GoalCategoryCreateView.as_view()),
    path("goal_category/list", categories.GoalCategoryListView.as_view()),
    path("goal_category/<pk>", categories.GoalCategoryView.as_view()),

    path("goal/create", goals.GoalCreateView.as_view()),
    path("goal/list", goals.GoalListView.as_view()),
    path("goal/<pk>", goals.GoalView.as_view()),


    #goal_category/{id}
]


