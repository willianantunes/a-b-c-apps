import logging
import uuid

from urllib.parse import urlparse

import requests

from django.db import DatabaseError
from django.db import connection
from django_stomp.builder import build_publisher
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceUnavailable

_logger = logging.getLogger(__name__)


def _extract_base_path(url):
    parsed_url = urlparse(url)
    base_path = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_path


def _make_request_to_external_service(healthcheck_class, path: str):
    # Define a reasonable timeout: 5 seconds to connect, 15 seconds to read
    timeout = (5, 10)
    try:
        response = requests.get(path, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        healthcheck_class.add_error(ServiceUnavailable(f"[HTTPError][{e.response.status_code}] - {path}"), e)
    except requests.exceptions.ConnectionError as e:
        healthcheck_class.add_error(ServiceUnavailable(f"[ConnectionError] - {path}"), e)
    except requests.exceptions.Timeout as e:
        healthcheck_class.add_error(ServiceUnavailable(f"[Timeout] - {path}"), e)
    except requests.exceptions.RequestException as e:
        healthcheck_class.add_error(ServiceUnavailable(f"[RequestException] - {path}"), e)
    except Exception as e:
        healthcheck_class.add_error(ServiceUnavailable(f"[Unknown error] - {path}"), e)


class DjangoSTOMPHealthCheck(BaseHealthCheckBackend):
    critical_service = True

    def check_status(self):
        subscription_id = str(uuid.uuid4())
        _logger.debug("Checking STOMP server health using subscription_id: %s", subscription_id)
        publisher = build_publisher()
        try:
            publisher.start()
            if not publisher.is_open():
                self.add_error(ServiceUnavailable("Unable to connect to STOMP server"))
        except ConnectionRefusedError as e:
            self.add_error(ServiceUnavailable("Connection has been refused"), e)
        except IOError as e:
            self.add_error(ServiceUnavailable("IOError"), e)
        except Exception as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)
        else:
            _logger.debug("Connection established. STOMP server is healthy.")
        finally:
            publisher.close()


class CustomDatabaseBackendHealthCheck(BaseHealthCheckBackend):
    critical_service = True

    def check_status(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            _logger.debug("Database is healthy.")
        except DatabaseError as e:
            self.add_error(ServiceUnavailable("Database error"), e)
        except Exception as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)
