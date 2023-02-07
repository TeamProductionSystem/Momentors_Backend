from django.urls import path, include
from team_production_system import views


path('api-auth/', include('rest_framework.urls',)),

# from .views import CustomUserCreateView


# urlpatterns = [
#     path('auth/register/', CustomUserCreateView.as_view(), name='register'),
# ]