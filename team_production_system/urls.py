from django.urls import path
from team_production_system import views


urlpatterns = [
    # User information end points
    #  path('user/<int:pk>/', views.CustomUserView.as_view(), name='user'),
    path('myprofile/', views.UserProfile.as_view(), name='my-profile'),

    # List of mentor and mentees end points
    path('mentor/', views.MentorList.as_view(), name='mentor-list'),
    path('mentee/', views.MenteeList.as_view(), name='mentee-list'),

    # End points related to sessions
    path('availabilty/', views.AvailabilityView.as_view(), name='availabilty'),
    path('sessionrequestform/',
         views.SessionRequestForm.as_view(), name='request-form'),
    path('session/', views.SessionView.as_view(), name='session'),
]
