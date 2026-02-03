from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count, Sum, Case, When, IntegerField, F
from django.utils import timezone
from django.db import transaction, IntegrityError
from datetime import timedelta

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeCreateSerializer


class PostListAPIView(APIView):
    def get(self, request):
        posts = (
            Post.objects
            .select_related("author")
            .annotate(like_count=Count("likes"))
            .order_by("-created_at")
        )
        return Response(PostSerializer(posts, many=True).data)


class PostDetailAPIView(APIView):
    def get(self, request, post_id):
        post = (
            Post.objects
            .select_related("author")
            .annotate(like_count=Count("likes"))
            .get(id=post_id)
        )

        comments = (
            Comment.objects
            .filter(post=post)
            .select_related("author")
            .order_by("created_at")
        )

        serialized = CommentSerializer(comments, many=True).data

        comment_map = {}
        for c in serialized:
            c["children"] = []
            comment_map[c["id"]] = c

        roots = []
        for c in serialized:
            if c["parent"]:
                comment_map[c["parent"]]["children"].append(c)
            else:
                roots.append(c)

        return Response({
            "post": PostSerializer(post).data,
            "comments": roots
        })


class LikeCreateAPIView(APIView):
    def post(self, request):
        serializer = LikeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                like, created = Like.objects.get_or_create(
                    user=serializer.validated_data["user"],
                    post=serializer.validated_data.get("post"),
                    comment=serializer.validated_data.get("comment"),
                )
        except IntegrityError:
            created = False

        return Response({"liked": created})


class LeaderboardAPIView(APIView):
    def get(self, request):
        since = timezone.now() - timedelta(hours=24)

        leaderboard = (
            Like.objects
            .filter(created_at__gte=since)
            .annotate(
                karma=Case(
                    When(post__isnull=False, then=5),
                    When(comment__isnull=False, then=1),
                    default=0,
                    output_field=IntegerField(),
                ),
                target_username=Case(
                    When(post__isnull=False, then=F("post__author__username")),
                    When(comment__isnull=False, then=F("comment__author__username")),
                ),
            )
            .values("target_username")
            .annotate(total_karma=Sum("karma"))
            .order_by("-total_karma")[:5]
        )

        return Response(leaderboard)
