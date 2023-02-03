from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Mentor, Mentee, User, Role

admin.site.register(User, UserAdmin)
admin.site.register(Mentor)
admin.site.register(Mentee)
admin.site.register(Role)

