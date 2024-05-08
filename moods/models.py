from django.db import models
from django.conf import settings
from django.db.models.functions.datetime import timezone
from django_sqids import SqidsField


class Mood(models.Model):
    sqid = SqidsField(real_field_name="id")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=75)
    icon = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.icon} {self.name}"


class Activity(models.Model):
    sqid = SqidsField(real_field_name="id")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=75)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "activities"


class Entry(models.Model):
    sqid = SqidsField(real_field_name="id")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    mood = models.ForeignKey(
        Mood,
        on_delete=models.CASCADE,
    )
    activities = models.ManyToManyField(
        Activity,
        blank=True,
    )

    note_title = models.CharField(max_length=255, blank=True)
    note_body = models.TextField(blank=True)

    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mood added at {self.date}:{self.time}"

    class Meta:
        verbose_name_plural = "entries"
        ordering = ["-date", "-time"]
