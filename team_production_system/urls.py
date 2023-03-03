from django.urls import path
from team_production_system import views


urlpatterns = [
     path('mentor/', views.MentorList.as_view(), name='mentor-list'),
     path('mentee/', views.MenteeList.as_view(), name='mentee-list'),
     path('sessionrequestform/', views.SessionRequestForm.as_view(), name='request-form'),
     path('user/<int:pk>/', views.CustomUserView.as_view(), name='user'),
     path('availabilty/', views.AvailabilityView.as_view(), name='availabilty'),
     path('session/', views.SessionView.as_view(), name='session'),
     path('myprofile/', views.UserProfile.as_view(), name='my-profile'),
]