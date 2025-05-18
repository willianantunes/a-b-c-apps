import fnmatch
import json
import logging
import os

import urllib3

from gevent import Timeout
from gevent import queue

# See why https://github.com/gevent/gevent/issues/1957#issuecomment-1902072588
urllib3.connectionpool.ConnectionPool.QueueCls = queue.LifoQueue

request_timeout = int(os.getenv("GUNICORN_CUSTOM_REQUEST_TIMEOUT", "60"))
logger = logging.getLogger("gunicorn.timeout")


class GunicornCustomTimeout:
    def __init__(self, timeout):
        self.timeout = timeout


timeout_route_ignore = json.loads(os.getenv("GUNICORN_TIMEOUT_ROUTES_IGNORE", "[]"))


def pre_request_timeout(worker, req):
    """
    Hook to enforce a total timeout for each request.
    Uses a per-request dictionary to store timeout state.
    """
    path_matches = any(fnmatch.fnmatch(req.path, pattern) for pattern in timeout_route_ignore)
    if path_matches:
        logger.debug("Ignoring timeout for request: %s, worker %s", req.path, worker.pid)
        return
    logger.debug("Starting timeout of %s seconds for request: %s, worker %s", request_timeout, req.path, worker.pid)
    # Using a custom exception to make sure the error will be caught by exception handlers
    req.timeout = Timeout(request_timeout, exception=CustomTimeoutExceededError)
    req.timeout.start()
    # Store timeout in worker's local storage
    if not hasattr(worker, "active_timeouts"):
        worker.active_timeouts = set()
    worker.active_timeouts.add(req.timeout)


def post_request_timeout(worker, req, environ, resp):
    """
    Hook to cancel and close the timeout after the request completes.
    """
    if hasattr(req, "timeout"):
        logger.debug(
            "Canceling and closing timeout for request: %s, worker %s",
            req.path,
            worker.pid,
        )
        req.timeout.cancel()
        req.timeout.close()
        if hasattr(worker, "active_timeouts"):
            worker.active_timeouts.discard(req.timeout)


def worker_exit_timeout(server, worker):
    """
    Hook called when a worker exits.
    """
    if hasattr(worker, "active_timeouts"):
        logger.debug(
            "Cleaning up %d active timeouts on shutdown for worker %s", len(worker.active_timeouts), worker.pid
        )
        for gevent_timeout in worker.active_timeouts:
            try:
                gevent_timeout.cancel()
                gevent_timeout.close()
            except gevent_timeout.TimeoutError:
                logger.exception("Error cleaning up timeout")
        worker.active_timeouts.clear()


class CustomTimeoutExceededError(Exception):
    """
    Exception raised when the custom timeout is exceeded.
    """
