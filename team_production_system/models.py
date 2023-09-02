# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.conf import settings
# from django.core.mail import send_mail
# from django.db.models.constraints import UniqueConstraint
# from phonenumber_field.modelfields import PhoneNumberField
# from multiselectfield import MultiSelectField
# from datetime import timedelta
# from django.core.files.storage import default_storage
# import random
# import secrets
# import pytz


# # Model for all users
# class CustomUser(AbstractUser):
#     is_mentor = models.BooleanField(default=False)
#     is_mentee = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     first_name = models.CharField(max_length=75)
#     last_name = models.CharField(max_length=75)
#     email = models.EmailField(max_length=75, unique=True)
#     phone_number = PhoneNumberField(
#         null=True, blank=True, unique=True, default=None)
#     profile_photo = models.ImageField(
#         upload_to='profile_photo', blank=True, null=True)

#     def __str__(self):
#         return self.username

#     def save(self, *args, **kwargs):
#         # Check if user is a new user
#         is_new_user = self.pk is None
#         self.username = self.username.lower()
#         super().save(*args, **kwargs)

#         if is_new_user:
#             # Instantiate notification model for new user
#             NotificationSettings.objects.create(user=self)
#             # Assign default photo to a new user
#             self.get_default_photo()
#             self.save()

#     def get_default_photo(self):
#         files = default_storage.listdir('random_photo')[1]
#         filename = random.choice(files)

#         with default_storage.open(f'random_photo/{filename}') as file:
#             self.profile_photo.save(filename, file, save=False)


# # The mentor model that allows the mentor to select skills
# # they know and information about them
# class Mentor(models.Model):

#     SKILLS_CHOICES = [
#         ('AI', 'AI'),
#         ('AWS S3', 'AWS S3'),
#         ('Bootstrap', 'Bootstrap'),
#         ('Career Help', 'Career Help'),
#         ('CSS', 'CSS'),
#         ('Django', 'Django'),
#         ('FastAPI', 'FastAPI'),
#         ('Git', 'Git'),
#         ('GitHub', 'GitHub'),
#         ('HTML', 'HTML'),
#         ('Insomnia', 'Insomnia'),
#         ('Interview Help', 'Interview Help'),
#         ('JavaScript', 'JavaScript'),
#         ('MUI', 'MUI'),
#         ('Other', 'Other'),
#         ('PostgreSQL', 'PostgreSQL'),
#         ('Postico', 'Postico'),
#         ('Python', 'Python'),
#         ('React', 'React'),
#         ('Resume Help', 'Resume Help'),
#         ('SQL', 'SQL'),
#         ('Time Management', 'Time Management'),
#         ('Vue.js', 'Vue.js'),
#     ]

#     user = models.OneToOneField(
#         CustomUser, on_delete=models.CASCADE, primary_key=True)
#     about_me = models.TextField(max_length=1000, default='')
#     skills = MultiSelectField(choices=SKILLS_CHOICES,
#                               max_choices=19, max_length=157, default='HTML')

#     def __str__(self):
#         return self.user.username


# # Model for mentees to input their team
# class Mentee(models.Model):
#     user = models.OneToOneField(
#         CustomUser, on_delete=models.CASCADE, primary_key=True)
#     team_number = models.IntegerField(default=0)

#     def __str__(self):
#         return self.user.username


# # Allow mentors to set their avaliabiltiy
# class Availability(models.Model):
#     mentor = models.ForeignKey(
#         Mentor, on_delete=models.CASCADE, related_name='mentor_availability')
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()

#     class Meta:
#         constraints = [
#             UniqueConstraint(
#                 fields=['mentor', 'start_time'], name='availability_constraint')
#         ]

#     def __str__(self):
#         return f"{self.mentor} is available from {self.start_time} to {self.end_time}."


# # The session model allows the mentee to setup a session and
# # allows both mentee and mentor see their sessions they have scheduled
# class Session(models.Model):
#     mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE,
#                                related_name='mentor_session')
#     mentor_availability = models.ForeignKey(
#         Availability, on_delete=models.CASCADE, related_name='mentor_session')
#     mentee = models.ForeignKey(
#         Mentee, on_delete=models.CASCADE, related_name='mentee_session')
#     start_time = models.DateTimeField()
#     project = models.CharField(max_length=500)
#     help_text = models.TextField(max_length=500)
#     git_link = models.URLField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     confirmed = models.BooleanField(default=False)
#     status_choices = [
#         ('Pending', 'Pending'),
#         ('Confirmed', 'Confirmed'),
#         ('Canceled', 'Canceled'),
#         ('Completed', 'Completed')
#     ]
#     # The mentee will be able to schedule a 30 minute or 60 minute session.
#     status = models.CharField(
#         max_length=10, choices=status_choices, default='Pending')
#     session_length_choices = [
#         (30, '30 minutes'),
#         (60, '60 minutes')
#     ]
#     session_length = models.IntegerField(
#         choices=session_length_choices, default=30)

#     def end_time(self):
#         return self.start_time + timedelta(minutes=self.session_length)

#     def __str__(self):
#         return f"{self.mentor_availability.mentor.user.username} session with {self.mentee.user.username} is ({self.status})"

#     # Notify a mentor that a mentee has requested a session
#     def mentor_session_notify(self):
#         # Define the timezone
#         est = pytz.timezone('US/Eastern')

#         # Convert the start time to EST
#         est_start_time = self.start_time.astimezone(est)

#         # Format the time and date
#         session_time = est_start_time.strftime('%-I:%M %p')
#         session_date = est_start_time.strftime('%A, %B %-d')

#         send_mail(
#             subject=(
#                 f'{self.mentee.user.first_name} {self.mentee.user.last_name} has requested your help'),
#             message=(f'{self.mentee.user.first_name} {self.mentee.user.last_name} from Team {self.mentee.team_number} has requested a {self.session_length}-minute mentoring session with you at {session_time} EST on {session_date}.'),
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[self.mentor.user.email],
#         )

#     # Create a a random string of characters to be used as a session code
#     def create_session_code(self):
#         # Set the start of the code to be 'MomentumMentorSession'
#         code = 'MomentumMentorSession'
#         # Append 20 random characters to the code
#         code += secrets.token_urlsafe(20)
#         return code

#     # Create a jitsi meeting link for the session with the randomly generated code
#     def create_meeting_link(self):
#         code = self.create_session_code()
#         return f'https://meet.jit.si/{code}'

#     # Notify the mentee and when the requested session has been confirmed
#     def mentee_confirm_notify(self, meeting_link):
#         # Define the timezone
#         est = pytz.timezone('US/Eastern')

#         # Convert the start time to EST
#         est_start_time = self.start_time.astimezone(est)

#         # Format the time and date
#         session_time = est_start_time.strftime('%-I:%M %p')
#         session_date = est_start_time.strftime('%A, %B %-d')

#         send_mail(
#             subject=('Mentor Session Confirmed'),
#             message=(f'A session with {self.mentee.user.first_name} and {self.mentor.user.first_name} has been confirmed for a {self.session_length}-minute mentoring session at {session_time} EST on {session_date}. Here is the link to your session: {meeting_link}'),
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[self.mentee.user.email]
#         )

#     # Notify the mentor when the requested session has been confirmed
#     def mentor_confirm_notify(self, meeting_link):
#         # Define the timezone
#         est = pytz.timezone('US/Eastern')

#         # Convert the start time to EST
#         est_start_time = self.start_time.astimezone(est)

#         # Format the time and date
#         session_time = est_start_time.strftime('%-I:%M %p')
#         session_date = est_start_time.strftime('%A, %B %-d')

#         send_mail(
#             subject=('Mentor Session Confirmed'),
#             message=(f'A session with {self.mentee.user.first_name} and {self.mentor.user.first_name} has been confirmed for a {self.session_length}-minute mentoring session at {session_time} EST on {session_date}. Here is the link to your session: {meeting_link}'),
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[self.mentor.user.email]
#         )

#     # Notify a mentor that a mentee has canceled a scheduled session
#     def mentor_cancel_notify(self):
#         # Define the timezone
#         est = pytz.timezone('US/Eastern')

#         # Convert the start time to EST
#         est_start_time = self.start_time.astimezone(est)

#         # Format the time and date
#         session_time = est_start_time.strftime('%-I:%M %p')
#         session_date = est_start_time.strftime('%A, %B %-d')

#         send_mail(
#             subject=(
#                 f'{self.mentee.user.first_name} {self.mentee.user.last_name} has canceled their session'),
#             message=(f'{self.mentee.user.first_name} {self.mentee.user.last_name} from Team {self.mentee.team_number} has canceled their {self.session_length}-minute mentoring session with you at {session_time} EST on {session_date}.'),
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[self.mentor.user.email],
#         )

#     # Notify a mentee that a mentor has canceled a scheduled session
#     def mentee_cancel_notify(self):
#         # Define the timezone
#         est = pytz.timezone('US/Eastern')

#         # Convert the start time to EST
#         est_start_time = self.start_time.astimezone(est)

#         # Format the time and date
#         session_time = est_start_time.strftime('%-I:%M %p')
#         session_date = est_start_time.strftime('%A, %B %-d')

#         send_mail(
#             subject=(
#                 f'{self.mentor.user.first_name} {self.mentor.user.last_name} has canceled your session'),
#             message=(f'{self.mentor.user.first_name} {self.mentor.user.last_name} has canceled the {self.session_length}-minute mentoring session with you at {session_time} EST on {session_date}.'),
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[self.mentee.user.email],
#         )

#     # Notify a user that a session is coming up in 60 min
#     # TODO: Needs unit testing
#     def sixty_min_notify(self):
#         # Define the timezone
#         est = pytz.timezone('US/Eastern')

#         # Convert the start time to EST
#         est_start_time = self.start_time.astimezone(est)

#         # Format the time and date
#         session_time = est_start_time.strftime('%-I:%M %p')

#         send_mail(
#             subject=('Mentor Session in 60 Minutes'),
#             message=(f'Your {self.session_length}-minute session with {self.mentee.user.first_name} and {self.mentor.user.first_name} at {session_time} EST is coming up in 60 minutes.'),
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[self.mentor.user.email, self.mentee.user.email],
#         )

#     # Notify a user that a session is coming up in 15 min
#     # TODO: Needs unit testing
#     def fifteen_min_notify(self):
#         # Define the timezone
#         est = pytz.timezone('US/Eastern')

#         # Convert the start time to EST
#         est_start_time = self.start_time.astimezone(est)

#         # Format the time and date
#         session_time = est_start_time.strftime('%-I:%M %p')

#         send_mail(
#             subject=('Mentor Session in 15 Minutes'),
#             message=(f'Your {self.session_length}-minute session with {self.mentee.user.first_name} and {self.mentor.user.first_name} at {session_time} EST is coming up in 15 minutes.'),
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[self.mentor.user.email, self.mentee.user.email],
#         )


# # Notification settings model that allows users to choose to be alerted when
# # they have a session requested, confirmed, or canceled.
# class NotificationSettings(models.Model):
#     user = models.OneToOneField(
#         CustomUser, on_delete=models.CASCADE, related_name='notification_settings')
#     session_requested = models.BooleanField(default=False)
#     session_confirmed = models.BooleanField(default=False)
#     session_canceled = models.BooleanField(default=False)
#     fifteen_minute_alert = models.BooleanField(default=False)
#     sixty_minute_alert = models.BooleanField(default=False)

#     def __str__(self):
#         return f'Notification settings for {self.user.first_name} {self.user.last_name}'
