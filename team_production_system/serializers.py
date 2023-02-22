from rest_framework import serializers
from .models import Mentor, Mentee, SessionRequestForm, CustomUser


# class CustomUserSerializer(serializers.ModelSerializer):
#     profile_photo = serializers.ImageField()

#     class Meta:
#         model = CustomUser
#         fields = [
#             'pk',
#             'username',
#             'first_name',
#             'last_name',
#             'email',
#             'phone_number',
#             'profile_photo',
#             'is_mentor',
#             'is_mentee',
#             'is_active',
#         ]

#     def update(self, instance, validated_data):
#         profile_photo = validated_data.get('profile_photo', None)
#         if profile_photo:
#             instance.profile_photo = profile_photo
#             instance.save()
#         return instance


class CustomUserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = [
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile_photo',
            'is_mentor',
            'is_mentee',
            'is_active',
        ]

    def update(self, instance, validated_data):
        # Extract the file data from the validated data
        profile_photo = validated_data.pop('profile_photo', None)
        
        # Call the parent update method to handle non-file fields
        instance = super().update(instance, validated_data)

        # If a new file was provided, create a new file instance and assign it to the model field
        if profile_photo:
            instance.profile_photo.save(profile_photo.name, profile_photo)
        
        return instance


class MentorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentor
        fields = ('first_name', 'last_name', 'email',
                  'about_me', 'skill', 'mentor_photo')


class MenteeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentee
        fields = ('first_name', 'last_name', 'email',
                  'about_me', 'team_number', 'mentor_photo')


class SessionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionRequestForm
        fields = ('project', 'help_text', 'git_link')
