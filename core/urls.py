from django.urls import path
from .views.teams_message_view import TeamsMessageView

urlpatterns = [
    path("teams/message/", TeamsMessageView.as_view()),
]
