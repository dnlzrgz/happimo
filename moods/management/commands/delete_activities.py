from moods.management.commands.base_delete_command import BaseDeleteCommand
from moods.models import Activity


class Command(BaseDeleteCommand):
    help = "Deletes activities for specified users."

    def delete_items(self, user):
        return Activity.objects.filter(user=user).delete()[0]

    @property
    def item_name(self):
        return "activities"
