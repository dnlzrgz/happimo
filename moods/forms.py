from django import forms
from moods.models import Entry, Mood


class EntryCreateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["mood", "activities", "note_title", "note_body", "date", "time"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mood"].queryset = Mood.objects.all()
