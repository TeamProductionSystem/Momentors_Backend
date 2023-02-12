from .models import Mentor, Mentee
from rest_framework import generics
from .serializers import  MentorListSerializer, MenteeListSerializer


class MentorList(generics.ListCreatAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorListSerializer


class MenteeList(generics.ListCreatAPIView):
    queryset = Mentee.objects.all()
    serializer_class = MenteeListSerializer