import random
from django.contrib.auth import get_user_model
from faker import Faker
from moods.models import Activity, Entry, Mood
from utils.dummy import FEELINGS_LIST, EMOJIS_LIST, ACTIVITY_LIST

fake = Faker()


def create_fake_user():
    credentials = {
        "username": fake.name(),
        "email": fake.email(),
        "password": fake.password(),
    }

    user = get_user_model().objects.create_user(**credentials)

    return (credentials, user)


def create_fake_entry(user, mood, activities=None):
    entry = Entry.objects.create(
        user=user,
        mood=mood,
        note_title=fake.sentence(),
        note_body=fake.paragraph(),
        date=fake.date(),
        time=fake.time(),
    )

    if activities:
        for activity in activities:
            entry.activities.add(*Activity.objects.filter(name__in=activity))

    return entry


def create_fake_mood(user):
    mood = Mood.objects.create(
        user=user,
        name=random.choice(FEELINGS_LIST),
        icon=random.choice(EMOJIS_LIST),
    )

    return mood


def create_fake_activity(user):
    activity = Activity.objects.create(
        user=user,
        name=random.choice(ACTIVITY_LIST),
    )

    return activity
