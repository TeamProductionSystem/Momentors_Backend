from django.urls import path
from team_production_system import views


urlpatterns = [
     path('mentors/', views.MentorList.as_view(), name='mentor-list'),
]