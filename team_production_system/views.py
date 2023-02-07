from djoser.views import UserCreateView
from rest_framework import generics
from .models import User, Mentor, Mentee
from .serializers import UserSerializer, MentorSerializer, MenteeSerializer

# class CustomUserCreateView(UserCreateView):
#     serializer_class = UserSerializer

#     def perform_create(self, serializer):
#         user = serializer.save()
#         is_mentor = self.request.data.get('is_mentor')
#         is_mentee = self.request.data.get('is_mentee')

#         if is_mentor:
#             Mentor.objects.create(user=user)
#         elif is_mentee:
#             Mentee.objects.create(user=user)

class MentorViewSet(generics.ListAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

class MenteeViewSet(generics.ListAPIView):
    queryset = Mentee.objects.all()
    serializer_class = MenteeSerializer