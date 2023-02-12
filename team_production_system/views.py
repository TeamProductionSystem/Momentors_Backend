from .models import Mentor
from rest_framework import generics
from .serializers import  MentorListSerializer


class MentorList(generics.ListAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorListSerializer