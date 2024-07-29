from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from utils.test import create_fake_activity


class Command(BaseCommand):
    help = "Creates a random list of activities for the specified users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            type=int,
            help="Number of activities",
            default=5,
        )

        parser.add_argument(
            "--users",
            nargs="+",
            type=str,
            help="List of users by username",
            required=True,
        )

    def handle(self, *args, **options):
        n = options.get("number")

        for username in options.get("users"):
            try:
                user = get_user_model().objects.get(username=username)

                for _ in range(n):
                    create_fake_activity(user=user)

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added {n} activities to {user}")
                )
            except get_user_model().DoesNotExist:
                raise CommandError(f"User {username} does not exist!")
