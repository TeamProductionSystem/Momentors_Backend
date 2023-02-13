from django.urls import path
from team_production_system import views


urlpatterns = [
     path('mentor/', views.MentorList.as_view(), name='mentor-list'),
     path('mentee/', views.MenteeList.as_view(), name='mentee-list'),
]