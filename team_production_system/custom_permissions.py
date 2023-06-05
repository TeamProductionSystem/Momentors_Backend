from rest_framework.permissions import BasePermission


class IsMentorMentee(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.pk == obj.mentor.pk or request.user.pk == obj.mentee.pk


class NotificationSettingsPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
