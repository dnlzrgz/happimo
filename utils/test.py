import random
from django.contrib.auth import get_user_model
from faker import Faker
from moods.models import Activity, Entry, Mood

fake = Faker()


def generate_activity() -> str:
    generators = [
        lambda: f"{fake.word(part_of_speech='verb').capitalize()} a {fake.word(part_of_speech='noun')}",
        lambda: f"{fake.word(part_of_speech='adjective').capitalize()} {fake.word(part_of_speech='noun')}",
        lambda: f"{fake.word(part_of_speech='verb').capitalize()} {fake.word(part_of_speech='adverb')}",
        lambda: f"{fake.word(part_of_speech='verb').capitalize()} with {fake.first_name()}",
        lambda: f"{fake.word(part_of_speech='adjective').capitalize()} {fake.job()}",
    ]

    return random.choice(generators)()


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
        name=fake.word().capitalize(),
        color=fake.color(),
    )

    return mood


def create_fake_activity(user):
    activity = Activity.objects.create(
        user=user,
        name=generate_activity(),
    )

    return activity
