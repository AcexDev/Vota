from django.urls import path
from .views import (homepage, add_vote, PollDetailView, PollCreateView, 
                    PollDeleteView, user_polls, poll_type_select,
                    create_text_poll)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('poll/<int:pk>/addvote/', add_vote, name='add-vote'),
    path('poll/new/', poll_type_select, name='create_poll'),
    path('poll/new/text', create_text_poll ,name='poll-create-text'),
    path('poll/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('poll/new/mcq', PollCreateView.as_view(), name='poll-create-mcq'),
    path('poll/<int:pk>/delete/', PollDeleteView.as_view(), name='delete-poll'),
    path('user_poll/', user_polls, name="user-polls")
]