from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Mentor,
    Mentee,
    CustomUser,
    Session,
    Availability,
    NotificationSettings
)

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Mentor)
admin.site.register(Mentee)
admin.site.register(Session)
admin.site.register(Availability)
admin.site.register(NotificationSettings)
