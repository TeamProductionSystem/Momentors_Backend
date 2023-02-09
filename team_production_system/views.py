from rest_framework import viewsets
from djoser.serializers import UserCreateSerializer
from team_production_system.serializers import UserSerializer
from django.contrib.auth.models import User

class CustomUserCreateView(viewsets.GenericViewSet):
    serializer_class = UserCreateSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()