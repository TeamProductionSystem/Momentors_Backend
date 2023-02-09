from rest_framework import serializers
from .models import User, Mentor, Mentee

class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['mentor', 'mentee'])
    skill = serializers.CharField(required=False)
    team_number = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name',
                  'last_name', 'phone_number', 'about_me', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            about_me=validated_data['about_me']
        )
        if validated_data['role'] == 'mentor':
            mentor = Mentor.objects.create(
                user=user, skill=validated_data['skill'])
        elif validated_data['role'] == 'mentee':
            mentee = Mentee.objects.create(
                user=user, team_number=validated_data['team_number'])

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'phone_number', 'about_me']
