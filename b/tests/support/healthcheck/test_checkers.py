from unittest import mock

import requests

from django.db import DatabaseError
from django.test import TestCase
from requests import HTTPError
from requests.exceptions import RequestException
from requests.exceptions import Timeout
from requests_mock import Mocker

from letter_b.support.healthcheck.checkers import CustomDatabaseBackendHealthCheck
from letter_b.support.healthcheck.checkers import DjangoSTOMPHealthCheck
from letter_b.support.healthcheck.checkers import _make_request_to_external_service


class TestDjangoSTOMPHealthCheck(TestCase):
    def test_healthcheck_behavior(self):
        # Act
        django_stomp_health_check = DjangoSTOMPHealthCheck()

        # Assert
        self.assertIsNone(django_stomp_health_check.check_status())

    @mock.patch("letter_b.support.healthcheck.checkers.build_publisher")
    def test_healthcheck_add_error_when_connection_not_is_open(self, mocked_build_publisher):
        # Arrange
        django_stomp_health_check = DjangoSTOMPHealthCheck()
        fake_publish_mock = mock.MagicMock()
        fake_publish_mock.is_open.return_value = False
        mocked_build_publisher.return_value = fake_publish_mock

        # Act
        django_stomp_health_check.check_status()

        # Assert
        self.assertEqual(len(django_stomp_health_check.errors), 1)
        self.assertEqual(str(django_stomp_health_check.errors[0]), "unavailable: Unable to connect to STOMP server")

    @mock.patch("letter_b.support.healthcheck.checkers.build_publisher")
    def test_healthcheck_add_error_when_connection_refused_is_raised(self, mocked_build_publisher):
        # Arrange
        django_stomp_health_check = DjangoSTOMPHealthCheck()
        fake_publish_mock = mock.MagicMock()
        fake_publish_mock.start.side_effect = ConnectionRefusedError("Connection has been refused")
        mocked_build_publisher.return_value = fake_publish_mock

        # Act
        django_stomp_health_check.check_status()

        # Assert
        self.assertEqual(len(django_stomp_health_check.errors), 1)
        self.assertEqual(str(django_stomp_health_check.errors[0]), "unavailable: Connection has been refused")

    @mock.patch("letter_b.support.healthcheck.checkers.build_publisher")
    def test_healthcheck_add_error_when_io_error_is_raised(self, mocked_build_publisher):
        # Arrange
        django_stomp_health_check = DjangoSTOMPHealthCheck()
        fake_publish_mock = mock.MagicMock()
        fake_publish_mock.start.side_effect = IOError("IOError")
        mocked_build_publisher.return_value = fake_publish_mock

        # Act
        django_stomp_health_check.check_status()

        # Assert
        self.assertEqual(len(django_stomp_health_check.errors), 1)
        self.assertEqual(str(django_stomp_health_check.errors[0]), "unavailable: IOError")

    @mock.patch("letter_b.support.healthcheck.checkers.build_publisher")
    def test_healthcheck_add_error_when_any_error_is_raised(self, mocked_build_publisher):
        # Arrange
        django_stomp_health_check = DjangoSTOMPHealthCheck()
        fake_publish_mock = mock.MagicMock()
        fake_publish_mock.start.side_effect = Exception("bald error")
        mocked_build_publisher.return_value = fake_publish_mock

        # Act
        django_stomp_health_check.check_status()

        # Assert
        self.assertEqual(len(django_stomp_health_check.errors), 1)
        self.assertEqual(str(django_stomp_health_check.errors[0]), "unavailable: Unknown error")


class TestCustomDatabaseBackendHealthCheck(TestCase):
    def test_healthcheck_behavior(self):
        # Act
        custom_database_backend_health_check = CustomDatabaseBackendHealthCheck()

        # Assert
        self.assertIsNone(custom_database_backend_health_check.check_status())

    @mock.patch("letter_b.support.healthcheck.checkers.connection.cursor")
    def test_make_request_to_external_service_add_correct_error_when_database_exception_is_raised(
        self, mock_connection
    ):
        # Arrange
        custom_database_backend_health_check = CustomDatabaseBackendHealthCheck()
        mock_connection.side_effect = DatabaseError("Fake database error")
        # Act
        custom_database_backend_health_check.check_status()

        # Assert
        self.assertEqual(len(custom_database_backend_health_check.errors), 1)
        self.assertEqual(str(custom_database_backend_health_check.errors[0]), "unavailable: Database error")

    @mock.patch("letter_b.support.healthcheck.checkers.connection.cursor")
    def test_make_request_to_external_service_add_correct_error_when_any_exception_is_raised(self, mock_connection):
        # Arrange
        custom_database_backend_health_check = CustomDatabaseBackendHealthCheck()
        mock_connection.side_effect = Exception("Fake error")

        # Act
        custom_database_backend_health_check.check_status()

        # Assert
        self.assertEqual(len(custom_database_backend_health_check.errors), 1)
        self.assertEqual(str(custom_database_backend_health_check.errors[0]), "unavailable: Unknown error")


class RequestToExternalServiceTestCase(TestCase):
    class FakeHealthCheck:
        def __init__(self):
            self.errors = []

        def add_error(self, error, exception):
            self.errors.append(error)

    @mock.patch("letter_b.support.healthcheck.checkers.requests.get")
    def test__make_request_to_external_service_add_correct_error_when_http_error_is_raised(self, mock_request):
        # Arrange
        fake_health_check = self.FakeHealthCheck()
        path = "https://fake.com"
        mock_response = mock.MagicMock()
        mock_response.status_code = 500
        mock_request.side_effect = HTTPError("HTTPError", response=mock_response)
        # Act
        _make_request_to_external_service(fake_health_check, path)
        # Assert
        self.assertEqual(len(fake_health_check.errors), 1)
        self.assertEqual(
            str(fake_health_check.errors[0]),
            f"unavailable: [HTTPError][500] - {path}",
        )

    def test__make_request_to_external_service_add_correct_error_when_response_status_code_is_500(self):
        # Arrange
        path = "https://fake.com"

        requests_mock = Mocker()
        requests_mock.get(
            path,
            status_code=500,
            json={"data": ""},
        )
        requests_mock.start()

        fake_health_check = self.FakeHealthCheck()

        # Act
        _make_request_to_external_service(fake_health_check, path)
        requests_mock.stop()

        # Assert
        self.assertEqual(len(fake_health_check.errors), 1)
        self.assertEqual(
            str(fake_health_check.errors[0]),
            f"unavailable: [HTTPError][500] - {path}",
        )

    def test__make_request_to_external_service_return_correct_json_parsed(self):
        # Arrange
        path = "https://fake.com"
        response_json = {"data": "fake data"}
        requests_mock = Mocker()
        requests_mock.get(
            path,
            status_code=200,
            json=response_json,
        )
        requests_mock.start()

        fake_health_check = self.FakeHealthCheck()

        # Act
        parsed_json_response = _make_request_to_external_service(fake_health_check, path)
        requests_mock.stop()

        # Assert
        self.assertEqual(len(fake_health_check.errors), 0)
        self.assertEqual(parsed_json_response, response_json)

    @mock.patch("letter_b.support.healthcheck.checkers.requests.get")
    def test__make_request_to_external_service_add_correct_error_when_connection_error_is_raised(self, mock_request):
        # Arrange
        fake_health_check = self.FakeHealthCheck()
        path = "https://fake.com"
        mock_request.side_effect = requests.exceptions.ConnectionError("Fake ConnectionError")

        # Act
        _make_request_to_external_service(fake_health_check, path)

        # Assert
        self.assertEqual(len(fake_health_check.errors), 1)
        self.assertEqual(
            str(fake_health_check.errors[0]),
            f"unavailable: [ConnectionError] - {path}",
        )

    @mock.patch("letter_b.support.healthcheck.checkers.requests.get")
    def test__make_request_to_external_service_add_correct_error_when_timeout_is_raised(self, mock_request):
        # Arrange
        fake_health_check = self.FakeHealthCheck()
        path = "https://fake.com"
        mock_request.side_effect = Timeout("Fake timeout")

        # Act
        _make_request_to_external_service(fake_health_check, path)

        # Assert
        self.assertEqual(len(fake_health_check.errors), 1)
        self.assertEqual(
            str(fake_health_check.errors[0]),
            f"unavailable: [Timeout] - {path}",
        )

    @mock.patch("letter_b.support.healthcheck.checkers.requests.get")
    def test__make_request_to_external_service_add_correct_error_when_request_exception_is_raised(self, mock_request):
        # Arrange
        fake_health_check = self.FakeHealthCheck()
        path = "https://fake.com"
        mock_request.side_effect = RequestException("Fake request exception")

        # Act
        _make_request_to_external_service(fake_health_check, path)

        # Assert
        self.assertEqual(len(fake_health_check.errors), 1)
        self.assertEqual(
            str(fake_health_check.errors[0]),
            f"unavailable: [RequestException] - {path}",
        )

    @mock.patch("letter_b.support.healthcheck.checkers.requests.get")
    def test__make_request_to_external_service_add_correct_error_when_base_exception_is_raised(self, mock_request):
        # Arrange
        fake_health_check = self.FakeHealthCheck()
        path = "https://fake.com"
        mock_request.side_effect = Exception("Fake base exception")

        # Act
        _make_request_to_external_service(fake_health_check, path)

        # Assert
        self.assertEqual(len(fake_health_check.errors), 1)
        self.assertEqual(
            str(fake_health_check.errors[0]),
            f"unavailable: [Unknown error] - {path}",
        )
