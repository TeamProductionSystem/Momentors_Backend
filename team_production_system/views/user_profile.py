import boto3
from django.conf import settings
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from team_production_system.models import CustomUser
from team_production_system.serializers import CustomUserSerializer

# View to update the user profile information


class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            return user
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({
                'error': 'An unexpected error occurred.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        user = self.request.user

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'is_mentor',
            'is_mentee',
            'is_active',
        ]

        for field in fields:
            if field in request.data:
                setattr(user, field, request.data[field])

        if 'profile_photo' in request.FILES:
            if user.profile_photo:
                s3 = boto3.client('s3')
                s3.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=user.profile_photo.name)

            user.profile_photo = request.FILES['profile_photo']

        user.save()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
