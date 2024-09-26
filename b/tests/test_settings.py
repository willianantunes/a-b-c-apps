from django.test import TestCase

from letter_b import settings


class TestMiddlewares(TestCase):
    def test_liveness_is_properly_configured(self):
        middlewares = settings.MIDDLEWARE
        expected_middleware = "letter_b.support.healthcheck.middlewares.LivenessHealthCheckMiddleware"
        self.assertEqual(middlewares[0], expected_middleware)
