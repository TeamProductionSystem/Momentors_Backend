from django.urls import path, include
from djoser import urls as djoser_urls
from .views import CustomUserCreateView, UserViewSet

urlpatterns = [
    path('', include(djoser_urls)),
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
]