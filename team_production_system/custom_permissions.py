from rest_framework.permissions import BasePermission


class IsMentorMentee(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_mentor = request.user.pk == obj.mentor.pk
        is_mentee = request.user.pk == obj.mentee.pk
        return is_mentor or is_mentee


class NotificationSettingsPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.mentor.user == request.user or request.user.is_staff
