import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from moods.models import Mood
from utils.dummy import FEELINGS_LIST

fake = Faker()


class Command(BaseCommand):
    help = "Creates a random list of moods for the specified users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            type=int,
            help="Number of moods",
            default=5,
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

                feelings = random.sample(FEELINGS_LIST, n)

                moods = [
                    Mood(
                        user=user,
                        name=feeling,
                        color=fake.color(),
                    )
                    for feeling in feelings
                ]

                Mood.objects.bulk_create(moods)

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added moods to {user}")
                )
            except get_user_model().DoesNotExist:
                raise CommandError(f"User {username} does not exist!")
