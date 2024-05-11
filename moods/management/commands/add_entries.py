import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from moods.models import Mood, Entry

fake = Faker()


class Command(BaseCommand):
    help = "Creates a random list of entries for the specified users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            type=int,
            help="Number of entries",
            default=100,
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

                moods = Mood.objects.all().filter(user=user)

                entries = [
                    Entry(
                        user=user,
                        mood=random.choice(moods),
                        note_title=fake.sentence(),
                        note_body=fake.paragraph(),
                        date=fake.date(),
                        time=fake.time(),
                    )
                    for _ in range(n)
                ]

                Entry.objects.bulk_create(entries)

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added entries to {user}")
                )
            except get_user_model().DoesNotExist:
                raise CommandError(f"User {username} does not exist!")
