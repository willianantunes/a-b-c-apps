import logging

from uuid import uuid4

from django.conf import settings
from django_stomp.builder import build_publisher
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from letter_b.apps.example.api.v1.serializers import PersonSerializer
from letter_b.apps.example.api.v1.serializers import TodoItemSerializer
from letter_b.apps.example.api.v1.serializers import UserAttributesSerializer
from letter_b.apps.example.models import AuditAction
from letter_b.apps.example.models import Person
from letter_b.apps.example.models import TodoItem

_logger = logging.getLogger(__name__)


class UserManagementAttributesAPIView(APIView):
    def post(self, request):
        user_id = uuid4()
        _logger.debug("The following user is trying to refresh his attributes: %s", user_id)
        serializer = UserAttributesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # testing logging trace
        _logger.info("What I received: %s", serializer.validated_data)

        # testing db trace
        AuditAction(user_id=user_id, action=UserManagementAttributesAPIView.post.__name__, success=True).save()

        # testing publish message to broker
        publisher = build_publisher(f"letter-b-views-{uuid4()}")
        publisher.send(
            queue=settings.CREATE_AUDIT_ACTION_DESTINATION,
            body={
                "user_id": user_id,
                "action": UserManagementAttributesAPIView.post.__name__,
                "success": True,
                "ip_address": "192.168.1.1",
            },
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        user_id = "Salted User has been logged"
        _logger.debug("The following user is trying to retrieve his attributes: %s", user_id)
        serializer = UserAttributesSerializer(
            {
                "full_name": "Carl Edward Sagan",
                "given_name": "Carl",
                "family_name": "Sagan",
                "user_metadata": {
                    "city": "santo andré",
                    "state": "alagoas",
                    "birthday": "23-06-1989",
                    "gender": "male",
                },
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
