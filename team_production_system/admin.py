from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Mentor, Mentee, User

admin.site.register(User, UserAdmin)
admin.site.register(Mentor)
admin.site.register(Mentee)


