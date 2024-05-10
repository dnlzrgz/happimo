from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from utils.test import (
    create_fake_entry,
    create_fake_mood,
    create_fake_user,
)
from utils.test_mixins import TestAuthenticatedViewAccessMixin
from moods.models import Entry


class EntryListViewTest(TestCase, TestAuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("entry_list")
        self.template_name = "moods/entry_list.html"

    def test_user_can_see_own_entries(self):
        self.client.login(**self.credentials)
        mood = create_fake_mood(self.user)
        entry = create_fake_entry(self.user, mood)

        response = self.client.get(self.url)

        self.assertContains(response, mood.icon)
        self.assertContains(response, mood.name)
        self.assertContains(response, entry.note_title)

    def test_user_can_not_see_other_users_entries(self):
        mood = create_fake_mood(self.user)
        entry = create_fake_entry(self.user, mood)

        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        response = self.client.get(self.url)

        self.assertNotContains(response, mood.icon)
        self.assertNotContains(response, mood.name)
        self.assertNotContains(response, entry.note_title)


class EntryCreateViewTest(TestCase, TestAuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("entry_create")
        self.template_name = "moods/entry_create_form.html"

    def test_authenticated_user_can_create_entry(self):
        self.client.login(**self.credentials)
        mood = create_fake_mood(self.user)
        entry_data = {
            "mood": mood.id,
            "note_title": "Testing.",
            "note_body": "Doing some testing.",
            "date": "2024-05-10",
            "time": "12:00:00",
        }

        response = self.client.post(self.url, data=entry_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(Entry.objects.count(), 1)


class EntryUpdateViewTest(TestCase, TestAuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.mood = create_fake_mood(self.user)
        self.entry = create_fake_entry(self.user, self.mood)
        self.url = reverse(
            "entry_update",
            kwargs={"slug": self.entry.sqid},
        )
        self.template_name = "moods/entry_update_form.html"

    def test_authenticated_user_can_update_entry(self):
        self.client.login(**self.credentials)
        new_entry_data = {
            "mood": self.mood.id,
            "note_title": "Testing.",
            "note_body": "Doing some testing.",
            "date": "2024-05-10",
            "time": "12:00:00",
        }

        response = self.client.post(self.url, data=new_entry_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.mood.refresh_from_db()
        self.assertTrue(
            Entry.objects.filter(
                note_title=new_entry_data["note_title"], user=self.user
            ).exists()
        )

    def test_user_can_not_update_other_users_entry(self):
        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        new_entry_data = {
            "mood": self.mood.id,
            "note_title": "Testing.",
            "note_body": "Doing some testing.",
            "date": "2024-05-10",
            "time": "12:00:00",
        }

        response = self.client.post(self.url, data=new_entry_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertFalse(
            Entry.objects.filter(note_title=new_entry_data["note_title"]).exists()
        )


class EntryDeleteViewTest(TestCase, TestAuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.mood = create_fake_mood(self.user)
        self.entry = create_fake_entry(self.user, self.mood)
        self.url = reverse(
            "entry_delete",
            kwargs={"slug": self.entry.sqid},
        )
        self.template_name = "moods/entry_delete_form.html"

    def test_owner_can_delete_entry(self):
        self.client.login(**self.credentials)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertFalse(Entry.objects.filter(pk=self.entry.pk).exists())

    def test_non_owner_cannot_delete_entry(self):
        new_entry = create_fake_entry(self.user, self.mood)
        new_entry_url = reverse(
            "entry_delete",
            kwargs={"slug": new_entry.sqid},
        )

        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        response = self.client.post(new_entry_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertTrue(Entry.objects.filter(pk=new_entry.pk).exists())
