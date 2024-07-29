from moods.management.commands.base_delete_command import BaseDeleteCommand
from moods.models import Entry


class Command(BaseDeleteCommand):
    help = "Deletes entries for specified users."

    def delete_items(self, user):
        return Entry.objects.filter(user=user).delete()[0]

    @property
    def item_name(self):
        return "entries"
