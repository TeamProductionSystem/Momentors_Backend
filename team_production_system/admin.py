from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Mentor, Mentee, CustomUser

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Mentor)
admin.site.register(Mentee)


