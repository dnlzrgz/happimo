from django.db import models
from django.db.models import Max
from django.db.models.functions.datetime import timezone
from django.core.validators import MinValueValidator
from django.conf import settings
from django.urls import reverse
from django_sqids import SqidsField
from moods.form_fields import ColorField


class Mood(models.Model):
    sqid = SqidsField(real_field_name="id")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=20)
    color = ColorField(default="#7542e6")
    relative_order = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
        ],
    )

    def get_absolute_url(self):
        return reverse("mood_update", kwargs={"slug": self.sqid})

    def save(self, *args, **kwargs):
        if not self.pk:
            max_order = Mood.objects.filter(user=self.user).aggregate(
                Max("relative_order")
            )["relative_order__max"]
            self.relative_order = (max_order or 0) + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["relative_order"]


class Activity(models.Model):
    sqid = SqidsField(real_field_name="id")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=75)

    def get_absolute_url(self):
        return reverse("activity_update", kwargs={"slug": self.sqid})

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "activities"
        ordering = ["name"]


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
        return f"Entry added at {self.date}:{self.time}"

    class Meta:
        verbose_name_plural = "entries"
        ordering = ["-date", "-time"]
