from .models import CustomUser, Mentee, SessionRequestForm, Availability
from .models import Session, Mentor
from rest_framework import generics, status
from .serializers import CustomUserSerializer, AvailabilitySerializer
from .serializers import SessionRequestSerializer, SessionSerializer
from .serializers import MentorListSerializer, MentorProfileSerializer
from .serializers import MenteeListSerializer, MenteeProfileSerializer
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse


# View to update the user profile information
class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = self.request.user
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return user


# View to see a list of all users flagged as a mentor
class MentorList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = CustomUser.objects.filter(is_mentor=True)

        if not queryset.exists():
            return Response({"message": "No mentors found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = MentorListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MentorFilteredList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        skills = self.kwargs['skills'].split(',')
        queryset = Mentor.objects.filter(skills__icontains=skills[0])
        for skill in skills[1:]:
            queryset = queryset.filter(skills__icontains=skill)

        if not queryset.exists():
            return Response({"message": "No mentors found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = MentorProfileSerializer(queryset, many=True)
        return Response(serializer.data)


# View to allow mentors to create and view the about me/skills.
class MentorInfoView(generics.ListCreateAPIView):
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Mentor.objects.filter(user=self.request.user)


# View to edit the logged in mentors about me and skills
class MentorInfoUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        return self.request.user.mentor


# View to see a list of all users flagged as a mentee
class MenteeList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            queryset = CustomUser.objects.filter(is_mentee=True)
        except Exception as e:
            return Response({"error": "Failed to retrieve mentee list."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not queryset:
            return Response({"message": "No mentees found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = MenteeListSerializer(queryset, many=True)
        response_data = serializer.data
        return Response(response_data)


# View to allow mentees to create and view the about me/skills.
class MenteeInfoView(generics.ListCreateAPIView):
    serializer_class = MenteeProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Mentee.objects.filter(user=self.request.user)


# View to edit the logged in mentees team number
class MenteeInfoUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenteeProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        return self.request.user.mentee


# Create and view all availabilities
class AvailabilityView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Exclude any availability that has an end time in the past
        return Availability.objects.filter(end_time__gte=timezone.now())

    def get(self, request):
        try:
            availabilities = self.get_queryset()

            # Check if there are any availabilities
            if not availabilities:
                return Response("No open availabilities.",
                                status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(availabilities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Error: Failed to retrieve availabilities.",
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Error: Failed to create availability.",
                            status=status.HTTP_400_BAD_REQUEST)


# View for mentees to submit session request forms.
# It is set to auto add the user who submited the form as request user.
class SessionRequestForm(generics.ListCreateAPIView):
    queryset = SessionRequestForm.objects.all()
    serializer_class = SessionRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response({'error':
                             'Failed to create session request form. Error: {}'.format(str(e))},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': 'Failed to create session request form. Error: {}'.format(str(e))},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Creat and view all sessions
class SessionView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]
