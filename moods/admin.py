from django.contrib import admin

from moods.models import Mood, Activity, Entry

admin.site.register(Mood)
admin.site.register(Activity)
admin.site.register(Entry)
