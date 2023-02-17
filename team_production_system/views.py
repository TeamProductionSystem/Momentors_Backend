from .models import CustomUser, Mentee, SessionRequestForm
from rest_framework import generics
from .serializers import CustomUserSerializer, MenteeListSerializer, SessionRequestSerializer
from django.db.models import Q


class CustomUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class MentorList(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_mentor=True)
        return queryset


class MenteeList(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_mentee=True)
        return queryset


class SessionRequestForm(generics.ListCreateAPIView):
    queryset = SessionRequestForm.objects.all()
    serializer_class = SessionRequestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
