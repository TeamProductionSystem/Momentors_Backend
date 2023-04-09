from django.urls import path
from team_production_system import views


urlpatterns = [
    # User information end points
    path('myprofile/', views.UserProfile.as_view(), name='my-profile'),

    # List of mentor end points
    path('mentor/', views.MentorList.as_view(), name='mentor-list'),
    path('mentorinfo/', views.MentorInfoView.as_view(), name='mentor-info'),
    path('mentor/<str:skills>/', views.MentorFilteredList.as_view(),
         name='mentor-filtered-list'),
    path('mentorinfoupdate/', views.MentorInfoUpdateView.as_view(),
         name='mentor-info-update'),


    # List of mentee end points
    path('mentee/', views.MenteeList.as_view(), name='mentee-list'),
    path('menteeinfo/', views.MenteeInfoView.as_view(), name='mentee-info'),
    path('menteeinfoupdate/', views.MenteeInfoUpdateView.as_view(),
         name='mentee-info-update'),

    # End points related to sessions
    path('availability/', views.AvailabilityView.as_view(),
         name='availability'),
    path('session/', views.SessionView.as_view(), name='session'),
]
