from .models import CustomUser, Mentee, SessionRequestForm, Availability, Session
from rest_framework import generics, status
from .serializers import CustomUserSerializer, SessionRequestSerializer, AvailabilitySerializer, SessionSerializer
from django.db.models import Q
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class CustomUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    parser_classes = (MultiPartParser, FormParser)

    def patch(self, request, pk, format=None):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class AvailabilityView(generics.ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer


class SessionView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user
