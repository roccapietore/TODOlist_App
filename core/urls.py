from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from core.views import SignUpView, LoginView, EditProfileView, UpdatePasswordView

urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('profile', EditProfileView.as_view()),
    path('update_password', UpdatePasswordView.as_view()),
    #path('login', csrf_exempt(LoginView.as_view())),
]

