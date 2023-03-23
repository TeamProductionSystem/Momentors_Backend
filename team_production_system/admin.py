from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Mentor, Mentee, CustomUser, SessionRequestForm, Session, Availability
# admin.site.register(UserAdmin)
admin.site.register(CustomUser)
admin.site.register(Mentor)
admin.site.register(Mentee)
admin.site.register(SessionRequestForm)
admin.site.register(Session)
admin.site.register(Availability)


