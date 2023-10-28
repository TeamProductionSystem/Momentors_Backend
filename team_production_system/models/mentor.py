from django.db import models
from multiselectfield import MultiSelectField

from .custom_user import CustomUser


# The mentor model that allows the mentor to select skills
# they know and information about them
class Mentor(models.Model):

    SKILLS_CHOICES = [
        ('AI', 'AI'),
        ('AWS S3', 'AWS S3'),
        ('Bootstrap', 'Bootstrap'),
        ('Career Help', 'Career Help'),
        ('CSS', 'CSS'),
        ('Django', 'Django'),
        ('FastAPI', 'FastAPI'),
        ('Git', 'Git'),
        ('GitHub', 'GitHub'),
        ('HTML', 'HTML'),
        ('Insomnia', 'Insomnia'),
        ('Interview Help', 'Interview Help'),
        ('JavaScript', 'JavaScript'),
        ('MUI', 'MUI'),
        ('Other', 'Other'),
        ('PostgreSQL', 'PostgreSQL'),
        ('Postico', 'Postico'),
        ('Python', 'Python'),
        ('React', 'React'),
        ('Resume Help', 'Resume Help'),
        ('SQL', 'SQL'),
        ('Time Management', 'Time Management'),
        ('Vue.js', 'Vue.js'),
    ]

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    about_me = models.TextField(max_length=1000, default='')
    team_number = models.IntegerField(default=0)
    skills = MultiSelectField(choices=SKILLS_CHOICES,
                              max_choices=19, max_length=157, default='HTML')

    def __str__(self):
        return self.user.username
