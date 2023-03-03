from .models import CustomUser, Mentee, SessionRequestForm, Availability, Session
from rest_framework import generics, status
from .serializers import CustomUserSerializer, SessionRequestSerializer, AvailabilitySerializer, SessionSerializer
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# View to update the user profile information 
class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user
    

# View for the users to load profile pictures 
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


# View to see a list of all users flagged as a mentor
class MentorList(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_mentor=True)
        return queryset


# View to see a list of all users flagged as a mentee
class MenteeList(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_mentee=True)
        return queryset


# View for mentees to submit session request forms. It is set to auto add the user who submited the form as request user.
class SessionRequestForm(generics.ListCreateAPIView):
    queryset = SessionRequestForm.objects.all()
    serializer_class = SessionRequestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Create and view all availabilities 
class AvailabilityView(generics.ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer


# Creat and view all sessions 
class SessionView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


