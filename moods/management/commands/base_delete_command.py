from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class BaseDeleteCommand(BaseCommand):
    help = "Base command for deleting items for specified users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            nargs="+",
            type=str,
            help="List of users by username",
            required=True,
        )

    def handle(self, *args, **options):
        for username in options.get("users"):
            try:
                user = get_user_model().objects.get(username=username)
                count = self.delete_items(user)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Deleted {count} {self.item_name} in total from {user}"
                    )
                )
            except get_user_model().DoesNotExist:
                raise CommandError(f"User {username} does not exist!")

    def delete_items(self, user):
        raise NotImplementedError("Subclasses must implement delete_items method")

    @property
    def item_name(self):
        raise NotImplementedError("Subclasses must implement item_name property")
