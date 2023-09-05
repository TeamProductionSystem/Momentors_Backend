from django.contrib import admin
from .models import (
    Mentor,
    Mentee,
    CustomUser,
    Session,
    Availability,
    NotificationSettings
)

# admin.site.register(UserAdmin)
admin.site.register(CustomUser)
admin.site.register(Mentor)
admin.site.register(Mentee)
admin.site.register(Session)
admin.site.register(Availability)
admin.site.register(NotificationSettings)
