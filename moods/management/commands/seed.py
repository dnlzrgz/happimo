import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from utils.test import create_fake_activity, create_fake_mood, create_fake_entry
from moods.models import Activity, Mood

fake = Faker()


class Command(BaseCommand):
    help = "Seeds the database with activities, moods, and entries for the specified users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            nargs="+",
            type=str,
            help="List of users by username",
            required=True,
        )
        parser.add_argument(
            "--activities",
            "-a",
            type=int,
            help="Number of activities to create",
            default=15,
        )
        parser.add_argument(
            "--moods",
            "-m",
            type=int,
            help="Number of moods to create",
            default=5,
        )
        parser.add_argument(
            "--entries",
            "-e",
            type=int,
            help="Number of entries to create",
            default=100,
        )

    def handle(self, *args, **options):
        for username in options["users"]:
            try:
                user = get_user_model().objects.get(username=username)

                for _ in range(options["activities"]):
                    create_fake_activity(user=user)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created {options['activities']} activities for {user}"
                    )
                )

                for _ in range(options["moods"]):
                    create_fake_mood(user)

                self.stdout.write(
                    self.style.SUCCESS(f"Created {options['moods']} moods for {user}")
                )

                moods = Mood.objects.filter(user=user)
                activities = Activity.objects.filter(user=user)
                for _ in range(options["entries"]):
                    mood = random.choice(moods)
                    create_fake_entry(
                        user,
                        mood,
                        random.sample(
                            list(activities),
                            random.randint(0, min(9, activities.count())),
                        ),
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created {options['entries']} entries for {user}"
                    )
                )

            except get_user_model().DoesNotExist:
                raise CommandError(f"User {username} does not exist!")

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))
