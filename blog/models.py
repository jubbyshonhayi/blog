from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def comment_count(self):
        return self.comments.count()



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE
    )

    date_posted = models.DateTimeField(default=timezone.now)

    def is_reply(self):
        return self.parent is not None


class NotificationQuerySet(models.QuerySet):
    def unread_for(self, user):
        if not user.is_authenticated:
            return self.none()

        return self.filter(user=user, is_read=False).select_related(
            'sender',
            'post',
            'comment',
        ).order_by('-timestamp')


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        User,
        related_name='sent_notifications',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        Comment,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    objects = NotificationQuerySet.as_manager()

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'is_read', '-timestamp']),
        ]

    def __str__(self):
        return self.message
