from django.urls import path

from moods.views.mood_views import (
    MoodCreateView,
    MoodDeleteView,
    MoodListView,
    MoodUpdateView,
)
from moods.views.activity_views import (
    ActivityCreateView,
    ActivityDeleteView,
    ActivityListView,
    ActivityUpdateView,
)

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
    path(
        "activities/",
        ActivityListView.as_view(),
        name="activity_list",
    ),
    path(
        "activities/create/",
        ActivityCreateView.as_view(),
        name="activity_create",
    ),
    path(
        "activities/update/<slug>",
        ActivityUpdateView.as_view(),
        name="activity_update",
    ),
    path(
        "activities/delete/<slug>",
        ActivityDeleteView.as_view(),
        name="activity_delete",
    ),
]
