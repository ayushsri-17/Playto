This document explains key architectural and technical decisions made in the implementation.

---

## 1. The Tree – Threaded Comments

### Data Modeling

Nested comments are modeled using an **adjacency list** approach:

- Each `Comment` belongs to a `Post`
- Each `Comment` may have a `parent` pointing to another `Comment`
- Root-level comments have `parent = NULL`

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )


## 2. The Math – Last 24h Leaderboard

The leaderboard is calculated dynamically from Like events, not stored counters.

Rules

Like on a post → 5 karma

Like on a comment → 1 karma

Only likes in the last 24 hours are counted

QuerySet Used
leaderboard = (
    Like.objects
    .filter(created_at__gte=timezone.now() - timedelta(hours=24))
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

## 3. The AI Audit – Example of AI Mistake and Fix

Issue

While using AI assistance, the initial leaderboard implementation attempted to annotate a User object and then traverse it:

target_user = Case(
    When(post__isnull=False, then="post__author"),
    When(comment__isnull=False, then="comment__author"),
)

.values("target_user__username")