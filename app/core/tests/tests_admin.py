"""
Test for Django admin notifications.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSideTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""

        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )

        self.client.force_login(self.admin)

        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test user'
        )

    def test_users_list(self):
        """Tests that users are listed on page."""

        url = reverse('admin:core_useraccount_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""

        url = reverse('admin:core_useraccount_change', args=(self.user.id,))
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the creation user page works."""

        url = reverse('admin:core_useraccount_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
