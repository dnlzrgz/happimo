import random
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from moods.models import Mood

fake = Faker()

FEELINGS_LIST = [
    "Happy",
    "Sad",
    "Angry",
    "Excited",
    "Anxious",
    "Content",
    "Depressed",
    "Euphoric",
    "Grateful",
    "Guilty",
    "Lonely",
    "Loved",
    "Melancholy",
    "Optimistic",
    "Proud",
    "Relaxed",
    "Stressed",
    "Surprised",
    "Tired",
    "Confused",
]

EMOJIS_LIST = [
    "😊",
    "😢",
    "😠",
    "😃",
    "😨",
    "😌",
    "😞",
    "😆",
    "😇",
    "😬",
    "😔",
    "😍",
    "😐",
    "😎",
    "😤",
    "😴",
    "😱",
    "😳",
    "😪",
    "🤔",
]


def create_fake_user():
    credentials = {
        "username": fake.name(),
        "email": fake.email(),
        "password": fake.password(),
    }

    user = get_user_model().objects.create_user(**credentials)

    return (credentials, user)


def create_fake_mood(user):
    mood = Mood.objects.create(
        user=user,
        name=random.choice(FEELINGS_LIST),
        icon=random.choice(EMOJIS_LIST),
    )

    return mood


class AuthenticatedViewAccessMixin:
    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        self.assertTemplateUsed(response, self.template_name)

    def test_unauthenticated_user_can_not_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)


class MoodListViewTest(TestCase, AuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("mood_list")
        self.template_name = "moods/mood_list.html"

    def test_user_can_see_own_moods(self):
        self.client.login(**self.credentials)
        mood = create_fake_mood(self.user)

        response = self.client.get(self.url)

        self.assertContains(response, mood.name)
        self.assertContains(response, mood.icon)

    def test_user_can_not_see_other_users_moods(self):
        mood = create_fake_mood(self.user)

        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        response = self.client.get(self.url)

        self.assertNotContains(response, mood.name)
        self.assertNotContains(response, mood.icon)


class MoodCreateViewTest(TestCase, AuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("mood_create")
        self.template_name = "moods/mood_create_form.html"

    def test_authenticated_user_can_create_mood(self):
        self.client.login(**self.credentials)
        mood_data = {
            "name": random.choice(FEELINGS_LIST),
            "icon": random.choice(EMOJIS_LIST),
        }

        response = self.client.post(self.url, data=mood_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertTrue(
            Mood.objects.filter(name=mood_data["name"], user=self.user).exists()
        )


class MoodUpdateViewTest(TestCase, AuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.mood = create_fake_mood(self.user)
        self.url = reverse(
            "mood_update",
            kwargs={"slug": self.mood.sqid},
        )
        self.template_name = "moods/mood_update_form.html"

    def test_authenticated_user_can_update_mood(self):
        self.client.login(**self.credentials)
        new_mood_data = {
            "icon": random.choice(EMOJIS_LIST),
            "name": random.choice(FEELINGS_LIST),
        }

        response = self.client.post(self.url, data=new_mood_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.mood.refresh_from_db()
        self.assertTrue(
            Mood.objects.filter(name=new_mood_data["name"], user=self.user).exists()
        )

    def test_user_can_not_update_other_users_moods(self):
        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        new_mood_data = {
            "name": random.choice(FEELINGS_LIST),
        }

        response = self.client.post(self.url, data=new_mood_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertFalse(Mood.objects.filter(name=new_mood_data["name"]).exists())


class MoodDeleteViewTest(TestCase, AuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.mood = create_fake_mood(self.user)
        self.url = reverse(
            "mood_delete",
            kwargs={"slug": self.mood.sqid},
        )
        self.template_name = "moods/mood_delete_form.html"

    def test_owner_can_delete_activity(self):
        self.client.login(**self.credentials)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertFalse(Mood.objects.filter(pk=self.mood.pk).exists())

    def test_non_owner_cannot_delete_activity(self):
        new_mood = create_fake_mood(self.user)
        new_mood_url = reverse(
            "mood_delete",
            kwargs={"slug": self.mood.sqid},
        )

        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        response = self.client.post(new_mood_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertTrue(Mood.objects.filter(pk=new_mood.pk).exists())
