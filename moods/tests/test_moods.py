import random
from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from moods.models import Mood
from utils.dummy import FEELINGS_LIST
from utils.test import create_fake_user, create_fake_mood
from utils.test_mixins import TestAuthenticatedViewAccessMixin


class MoodListViewTest(TestCase, TestAuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("mood_list")
        self.template_name = "moods/mood_list.html"

    def test_user_can_see_own_moods(self):
        self.client.login(**self.credentials)
        mood = create_fake_mood(self.user)

        response = self.client.get(self.url)

        self.assertContains(response, mood.name)
        self.assertContains(response, mood.color)

    def test_user_can_not_see_other_users_moods(self):
        mood = create_fake_mood(self.user)

        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        response = self.client.get(self.url)

        self.assertNotContains(response, mood.name)
        self.assertNotContains(response, mood.color)


class MoodCreateViewTest(TestCase, TestAuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("mood_create")
        self.template_name = "moods/mood_create_form.html"

    def test_authenticated_user_can_create_mood(self):
        self.client.login(**self.credentials)
        mood_data = {
            "name": random.choice(FEELINGS_LIST),
            "color": "#145465",
        }

        response = self.client.post(self.url, data=mood_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertTrue(
            Mood.objects.filter(name=mood_data["name"], user=self.user).exists()
        )

    def test_correct_relative_order(self):
        for i in range(5):
            mood = create_fake_mood(self.user)
            self.assertEqual(mood.relative_order, i + 1)


class MoodUpdateViewTest(TestCase, TestAuthenticatedViewAccessMixin):
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
            "name": random.choice(FEELINGS_LIST),
            "color": "#ff0000",
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


class MoodDeleteViewTest(TestCase, TestAuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.mood = create_fake_mood(self.user)
        self.url = reverse(
            "mood_delete",
            kwargs={"slug": self.mood.sqid},
        )
        self.template_name = "moods/mood_delete_form.html"

    def test_owner_can_delete_mood(self):
        self.client.login(**self.credentials)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertFalse(Mood.objects.filter(pk=self.mood.pk).exists())

    def test_non_owner_cannot_delete_mood(self):
        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertTrue(Mood.objects.filter(pk=self.mood.pk).exists())
