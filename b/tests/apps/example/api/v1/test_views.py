from django.test import TestCase

from letter_b.apps.example.models import AuditAction
from tests.utils import is_valid_uuid


class TestUserView(TestCase):
    def test_should_return_400_as_no_property_has_been_sent(self):
        # Arrange
        fake_data = {}
        # Act
        response = self.client.post("/api/v1/users/attributes", content_type="application/json", data=fake_data)
        # Assert
        body = response.json()
        self.assertEqual(response.status_code, 400)
        request_id = body["error"]["requestId"]
        self.assertEqual(
            body,
            {
                "error": {
                    "field_related_errors": {"non_field_errors": ["At least one property should be set!"]},
                    "requestId": request_id,
                },
                "status_code": 400,
                "type": "VALIDATION_ERRORS",
            },
        )

    def test_should_return_200_with_new_full_name(self):
        # Arrange
        fake_data = {
            "full_name": "Jafar Iago",
            "user_metadata": {"birthday": "1985-06-23"},
        }
        # Act
        response = self.client.post("/api/v1/users/attributes", content_type="application/json", data=fake_data)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AuditAction.objects.count(), 1)
        created_audit_action: AuditAction = AuditAction.objects.first()
        self.assertTrue(is_valid_uuid(created_audit_action.id))
        self.assertIsNone(created_audit_action.ip_address)
        self.assertEqual(created_audit_action.action, "post")
        self.assertTrue(created_audit_action.success)

    def test_should_return_200_with_user_attributes(self):
        # Act
        response = self.client.get("/api/v1/users/attributes", content_type="application/json")
        # Assert
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(
            body,
            {
                "user_metadata": {
                    "city": "santo andré",
                    "state": "alagoas",
                    "birthday": "23-06-1989",
                    "gender": "male",
                },
                "full_name": "Carl Edward Sagan",
                "given_name": "Carl",
                "family_name": "Sagan",
            },
        )
