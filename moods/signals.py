from django.db.models import F
from django.db.models.signals import post_delete
from django.dispatch import receiver
from moods.models import Mood


@receiver(post_delete, sender=Mood)
def reorder_moods(sender, instance, **kwargs):
    Mood.objects.filter(
        user=instance.user, relative_order__gt=instance.relative_order
    ).update(relative_order=F("relative_order") - 1)
