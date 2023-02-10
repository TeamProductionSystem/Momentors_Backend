from rest_framework import serializers
from .models import Mentor, Mentee

class MentorListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mentor
        fields = ('first_name', 'last_name', 'email',
                  'about_me', 'skill', 'mentor_photo')