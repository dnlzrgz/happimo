import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from moods.models import Activity, Mood, Entry

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
                activities = Activity.objects.all().filter(user=user)

                for _ in range(n):
                    mood = random.choice(moods)

                    entry = Entry.objects.create(
                        user=user,
                        mood=mood,
                        note_title=fake.sentence(),
                        note_body=fake.paragraph(),
                        date=fake.date(),
                        time=fake.time(),
                    )

                    random_activities = random.sample(
                        list(activities), random.randint(0, 3)
                    )
                    entry.activities.add(*random_activities)
                    entry.save()

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added entries to {user}")
                )
            except get_user_model().DoesNotExist:
                raise CommandError(f"User {username} does not exist!")
