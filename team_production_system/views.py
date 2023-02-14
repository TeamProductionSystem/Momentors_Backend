from .models import Mentor, Mentee, SessionRequestForm
from rest_framework import generics
from .serializers import MentorListSerializer, MenteeListSerializer, SessionRequestSerializer


class MentorList(generics.ListCreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorListSerializer


class MenteeList(generics.ListCreateAPIView):
    queryset = Mentee.objects.all()
    serializer_class = MenteeListSerializer


class SessionRequestForm(generics.ListCreateAPIView):
    queryset = SessionRequestForm.objects.all()
    serializer_class = SessionRequestSerializer
