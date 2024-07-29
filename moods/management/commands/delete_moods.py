from moods.management.commands.base_delete_command import BaseDeleteCommand
from moods.models import Mood


class Command(BaseDeleteCommand):
    help = "Deletes moods for specified users."

    def delete_items(self, user):
        return Mood.objects.filter(user=user).delete()[0]

    @property
    def item_name(self):
        return "moods"
