from django.urls import path

from moods.views import MoodCreateView, MoodDeleteView, MoodListView, MoodUpdateView

urlpatterns = [
    path(
        "moods/",
        MoodListView.as_view(),
        name="mood_list",
    ),
    path(
        "moods/create/",
        MoodCreateView.as_view(),
        name="mood_create",
    ),
    path(
        "moods/update/<slug>",
        MoodUpdateView.as_view(),
        name="mood_update",
    ),
    path(
        "moods/delete/<slug>",
        MoodDeleteView.as_view(),
        name="mood_delete",
    ),
]
