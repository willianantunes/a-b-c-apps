from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase


class TestUserManagement(TestCase):
    def test_should_do_nothing_when_seed_is_called_with_no_parameters(self):
        out = StringIO()
        call_command("seed", stdout=out)

        self.assertFalse(bool(out.getvalue()))
        self.assertEqual(User.objects.filter(username="admin").count(), 0)

    def test_should_create_super_user_only(self):
        out = StringIO()
        call_command("seed", "--create-super-user", stdout=out)

        self.assertEqual(out.getvalue(), "Creating ADMIN username admin\n")
        self.assertEqual(User.objects.filter(username="admin").count(), 1)
