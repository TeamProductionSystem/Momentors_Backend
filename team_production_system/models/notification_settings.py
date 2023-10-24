from django.db import models


# Notification settings model that allows users to choose to be alerted when
# they have a session requested, confirmed, or canceled.
class NotificationSettings(models.Model):
    user = models.OneToOneField(
        "team_production_system.CustomUser",
        on_delete=models.CASCADE,
        related_name='notification_settings',
    )
    session_requested = models.BooleanField(default=False)
    session_confirmed = models.BooleanField(default=False)
    session_canceled = models.BooleanField(default=False)
    fifteen_minute_alert = models.BooleanField(default=False)
    sixty_minute_alert = models.BooleanField(default=False)

    def __str__(self):
        return (
            f'Notification settings for '
            f'{self.user.first_name} {self.user.last_name}'
        )
