from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import User
from core.serializers import CreateUserSerializer, LoginSerializer, UserSerializer, UpdatePasswordSerializer
from django.contrib.auth import login, logout


class SignUpView(CreateAPIView):
    model = User
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        ret = super().post(request, *args, **kwargs)
        user = User.objects.get(username=ret.data['username'])
        login(request, user=user, backend='django.contrib.auth.backends.ModelBackend')
        return ret


class LoginView(CreateAPIView):
    model = User
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        s: LoginSerializer = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        username = s.validated_data["username"]
        user = User.objects.get(username=username)
        login(request, user=user, backend='django.contrib.auth.backends.ModelBackend')
        user_serializer = UserSerializer(instance=user)
        return Response(user_serializer.data)


class EditProfileView(RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({})


class UpdatePasswordView(UpdateAPIView):
    model = User
    serializer_class = UpdatePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        ret = super().update(request, *args, **kwargs)
        login(request, user=request.user, backend='django.contrib.auth.backends.ModelBackend')
        return ret

