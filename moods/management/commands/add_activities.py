import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from moods.models import Activity
from utils.dummy import ACTIVITY_LIST


class Command(BaseCommand):
    help = "Creates a random list of activities for the specified users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            type=int,
            help="Number of activities",
            default=len(ACTIVITY_LIST) // 2,
        )

        parser.add_argument(
            "--users",
            nargs="+",
            type=str,
            help="List of users by username",
        )

    def handle(self, *args, **options):
        n = options.get("number")

        for username in options.get("users"):
            try:
                user = get_user_model().objects.get(username=username)

                activities = [
                    Activity(
                        user=user,
                        name=activity,
                    )
                    for activity in random.sample(ACTIVITY_LIST, n)
                ]

                Activity.objects.bulk_create(activities)

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added activities to {user}")
                )
            except get_user_model().DoesNotExist:
                raise CommandError(f"User {username} does not exist!")
