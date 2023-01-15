from django.urls import path, include
from team_production_system import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls',)),
]
