from django.urls import path, include
from .views import UserCreateView, MentorViewSet, MenteeViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'mentors', MentorViewSet)
router.register(r'mentees', MenteeViewSet)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('', include(router.urls)),
]