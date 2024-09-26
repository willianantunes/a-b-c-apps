from django.test import TestCase


class TestRoutes(TestCase):
    def test_healthcheck_readiness_urls_exists(self):
        # Act
        response = self.client.get("/api/healthcheck/readiness/?format=json")
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_healthcheck_liveness_urls_exists(self):
        # Act
        response = self.client.get("/api/healthcheck/liveness")
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_healthcheck_integrations_urls_exists(self):
        # Act
        response = self.client.get("/api/healthcheck/integrations/?format=json")
        # Assert
        self.assertEqual(len(response.json()), 2)
