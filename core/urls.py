from django.urls import path
from core.views import SignUpView, LoginView, EditProfileView, UpdatePasswordView

urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('profile', EditProfileView.as_view()),
    path('update_password', UpdatePasswordView.as_view()),

]

