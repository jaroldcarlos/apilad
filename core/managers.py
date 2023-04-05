from django.utils import timezone
from django.db import models
from django.db.models import Q, Count


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(active=True)


class PublishedManager(models.Manager):
    def get_queryset(self):
        objects = super(PublishedManager, self).get_queryset()
        objects = objects.filter(status='p')
        objects = objects.filter(
            Q(published_at__isnull=True) |
            (Q(published_at__isnull=False) & Q(published_at__lte=timezone.now()))
        )
        objects = objects.filter(
            Q(expired_at__isnull=True) |
            (Q(expired_at__isnull=False) & Q(expired_at__gt=timezone.now()))
        )
        return objects


class ReadOnlyManager(models.Manager):
    def update(self, *args, **kwargs):
        pass

class InUseManager(models.Manager):
    def get_queryset(self):
        objects = super(InUseManager, self).get_queryset()
        objects = objects.annotate(
            posts_count=Count(
                "posts",
                filter=Q(posts__status='p')
            )
        ).filter(posts_count__gt=0)
        return objects

class IsApprovedManager(models.Manager):
    def get_queryset(self):
        objects = super(IsApprovedManager, self).get_queryset()
        return objects.filter(approved=True)
