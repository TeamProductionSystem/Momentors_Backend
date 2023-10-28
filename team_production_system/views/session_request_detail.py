from rest_framework import generics

from team_production_system.custom_permissions import IsMentorMentee
from team_production_system.models import Session
from team_production_system.serializers import SessionSerializer


class SessionRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsMentorMentee]

    # Update the session status
    def perform_update(self, serializer):
        session = serializer.instance
        status = self.request.data.get('status')

        # Notify users if session is canceled
        if status == 'Canceled':
            session.status = status
            session.save()

            # If mentee cancels session, check mentor notification
            if self.request.user.is_mentee and \
                    session.mentor.user.notification_settings.session_canceled:
                session.mentor_cancel_notify()

            # If mentor cancels session, check mentee notification

            elif self.request.user.is_mentor and \
                    session.mentee.user.notification_settings.session_canceled:
                session.mentee_cancel_notify()

        # Notify mentee when a mentor confirms session request
        elif status == 'Confirmed':
            session.status = status
            meeting_link = session.create_meeting_link()
            session.save()

            # Check mentee's notification settings before notifying
            if session.mentee.user.notification_settings.session_confirmed:
                session.mentee_confirm_notify(meeting_link)

            # Check mentor's notification settings before notifying
            if session.mentor.user.notification_settings.session_confirmed:
                session.mentor_confirm_notify(meeting_link)

        else:
            serializer.save()
