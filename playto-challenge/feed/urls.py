from django.urls import path
from .views import (
    PostListAPIView,
    PostDetailAPIView,
    LikeCreateAPIView,
    LeaderboardAPIView,
)

urlpatterns = [
    path("posts/", PostListAPIView.as_view()),
    path("posts/<int:post_id>/", PostDetailAPIView.as_view()),
    path("likes/", LikeCreateAPIView.as_view()),
    path("leaderboard/", LeaderboardAPIView.as_view()),
]
