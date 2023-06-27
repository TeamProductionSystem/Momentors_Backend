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
    path('availability/', views.AvailabilityListCreateView.as_view(), name='availability'),
    # Delete availability
    path('availability/<int:pk>/', views.AvailabilityDeleteView.as_view(),
         name='availability-delete'),
    path('session/', views.SessionView.as_view(), name='session'),
    path('archivesession/', views.ArchiveSessionView.as_view(),
         name='archive-session'),
    path('sessionrequest/', views.SessionRequestView.as_view(),
         name='session'),
    path('sessionrequest/<int:pk>/', views.SessionRequestDetailView.as_view(),
         name='session-detail'),
    path('sessionsignuplist/', views.SessionSignupListView.as_view(),
         name='session-signup-list'),
    path('notificationsettings/<int:pk>/', views.NotificationSettingsView.as_view(),
         name='notification-settings'),
]
