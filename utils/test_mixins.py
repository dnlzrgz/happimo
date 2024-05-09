from http import HTTPStatus


class TestAuthenticatedViewAccessMixin:
    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        self.assertTemplateUsed(response, self.template_name)

    def test_unauthenticated_user_can_not_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
