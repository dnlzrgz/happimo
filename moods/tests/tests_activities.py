import random
from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from moods.models import Activity
from utils.dummy import ACTIVITY_LIST
from utils.test import create_fake_user, create_fake_activity
from utils.test_mixins import TestAuthenticatedViewAccessMixin


class ActivityListViewTest(TestCase, TestAuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("activity_list")
        self.template_name = "moods/activity_list.html"

    def test_user_can_see_own_activities(self):
        self.client.login(**self.credentials)
        activity = create_fake_activity(self.user)

        response = self.client.get(self.url)

        self.assertContains(response, activity.name)

    def test_user_can_not_see_other_users_activities(self):
        activity = create_fake_activity(self.user)

        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        response = self.client.get(self.url)

        self.assertNotContains(response, activity.name)


class ActivityCreateViewTest(TestCase, TestAuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("activity_create")
        self.template_name = "moods/activity_create_form.html"

    def test_authenticated_user_can_create_activity(self):
        self.client.login(**self.credentials)
        activity_data = {
            "name": random.choice(ACTIVITY_LIST),
        }

        response = self.client.post(self.url, data=activity_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertTrue(
            Activity.objects.filter(name=activity_data["name"], user=self.user).exists()
        )


class ActivityUpdateViewTest(TestCase, TestAuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.activity = create_fake_activity(self.user)
        self.url = reverse(
            "activity_update",
            kwargs={"slug": self.activity.sqid},
        )
        self.template_name = "moods/activity_update_form.html"

    def test_authenticated_user_can_update_activity(self):
        self.client.login(**self.credentials)
        new_activity_data = {
            "name": random.choice(ACTIVITY_LIST),
        }

        response = self.client.post(self.url, data=new_activity_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.activity.refresh_from_db()
        self.assertTrue(
            Activity.objects.filter(
                name=new_activity_data["name"], user=self.user
            ).exists()
        )

    def test_user_can_not_update_other_users_activities(self):
        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        new_activity_data = {
            "name": random.choice(ACTIVITY_LIST),
        }

        response = self.client.post(self.url, data=new_activity_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertFalse(
            Activity.objects.filter(name=new_activity_data["name"]).exists()
        )


class ActivityDeleteViewTest(TestCase, TestAuthenticatedViewAccessMixin):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.activity = create_fake_activity(self.user)
        self.url = reverse(
            "activity_delete",
            kwargs={"slug": self.activity.sqid},
        )
        self.template_name = "moods/activity_delete_form.html"

    def test_owner_can_delete_activity(self):
        self.client.login(**self.credentials)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertFalse(Activity.objects.filter(pk=self.activity.pk).exists())

    def test_non_owner_cannot_delete_activity(self):
        new_activity = create_fake_activity(self.user)
        new_activity_url = reverse(
            "activity_delete",
            kwargs={"slug": self.activity.sqid},
        )

        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        response = self.client.post(new_activity_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        self.assertTrue(Activity.objects.filter(pk=new_activity.pk).exists())
