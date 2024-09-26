import uuid

from unittest import mock

from django.test import TestCase
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from tests.utils import is_valid_uuid


class TestingPurposeAuthentication(authentication.BaseAuthentication):
    def __init__(self):
        super().__init__()

    def authenticate(self, request):
        raise exceptions.AuthenticationFailed("Forcing an honest but justifiable authentication exception")


class TestingPurposeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=70, required=True)
    family_name = serializers.CharField(max_length=35, required=True)


class TestingPurposeAPIView(APIView):
    def get(self, request):
        raise Exception

    def post(self, request):
        deserializer = TestingPurposeSerializer(data={})
        deserializer.is_valid(raise_exception=True)

    def put(self, request):
        raise TestingPurposeAPIException


class TestingPurposeWithAuthenticationAPIView(APIView):
    authentication_classes = [TestingPurposeAuthentication]

    def get(self, request):
        pass


class TestingPurposeAPIException(exceptions.APIException):
    status_code = status.HTTP_510_NOT_EXTENDED
    default_detail = "You are late"
    default_code = "Invalid sheet format", "invalid_sheet_format"


class TestGlobalExceptionHandlerRequestIDConfiguration(TestCase):
    @mock.patch("letter_b.apps.example.api.v1.views.APIView.initial")
    def test_should_return_default_message_error_with_generated_request_id(self, mock_initial):
        # Arrange
        request_path = "/api/v1/users/attributes"
        headers = {"Authorization": "Aladdin"}
        mock_initial.side_effect = Exception
        # Act
        response = self.client.get(request_path, headers=headers)
        # Assert
        self.assertEqual(response.status_code, 500)
        body = response.json()
        request_id = body["error"]["requestId"]
        self.assertTrue(is_valid_uuid(request_id))
        self.assertEqual(
            body,
            {
                "error": {
                    "msg": f'Oh, sorry! We didn\'t expect that 😬 Please inform the ID "{request_id}" so we can help you properly.',  # noqa: E501
                    "requestId": request_id,
                },
                "status_code": 500,
                "type": "UNEXPECTED_ERROR",
            },
        )


class TestGlobalExceptionHandlerUnitTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.request_id = str(uuid.uuid4())
        self.request_id_patcher = mock.patch(
            "letter_b.apps.example.api.global_exception_handler.current_request_id",
            return_value=self.request_id,
        )
        self.mock_request_id = self.request_id_patcher.start()

    def tearDown(self):
        self.request_id_patcher.stop()

    def test_should_return_message_when_unhandled_exception_is_raised(self):
        # Arrange
        request = self.factory.get("/api/v1/agrabah")
        view = TestingPurposeAPIView.as_view()
        # Act
        response = view(request)
        # Assert
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.data,
            {
                "error": {
                    "msg": f'Oh, sorry! We didn\'t expect that 😬 Please inform the ID "{self.request_id}" so we can help you properly.',  # noqa: E501
                    "requestId": self.request_id,
                },
                "status_code": 500,
                "type": "UNEXPECTED_ERROR",
            },
        )

    def test_should_return_message_when_validation_exception_is_raised(self):
        # Arrange
        request = self.factory.post("/api/v1/eru-iluvatar")
        view = TestingPurposeAPIView.as_view()
        # Act
        response = view(request)
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "error": {
                    "field_related_errors": {
                        "name": ["This field is required."],
                        "family_name": ["This field is required."],
                    },
                    "requestId": self.request_id,
                },
                "status_code": 400,
                "type": "VALIDATION_ERRORS",
            },
        )

    def test_should_return_message_when_exception_from_drf_pipeline_is_raised_through_authentication(self):
        # Arrange
        request = self.factory.post("/api/v1/gandalf")
        view = TestingPurposeWithAuthenticationAPIView.as_view()
        # Act
        response = view(request)
        # Assert
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data,
            {
                "error": {
                    "msg": "Forcing an honest but justifiable authentication exception",
                    "requestId": self.request_id,
                },
                "status_code": 403,
                "type": "AUTHENTICATION_FAILED",
            },
        )

    def test_should_return_message_when_api_exception_is_raised(self):
        # Arrange
        request = self.factory.put("/api/v1/gandalf")
        view = TestingPurposeAPIView.as_view()
        # Act
        response = view(request)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_510_NOT_EXTENDED)
        self.assertEqual(
            response.data,
            {
                "error": {"msg": "You are late", "requestId": self.request_id},
                "status_code": 510,
                "type": "INVALID_SHEET_FORMAT",
            },
        )
