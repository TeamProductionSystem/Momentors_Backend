from rest_framework import serializers
from .models import Mentor, Mentee, SessionRequestForm

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