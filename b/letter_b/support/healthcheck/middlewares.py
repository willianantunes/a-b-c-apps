from django.http import JsonResponse


class LivenessHealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/api/healthcheck/liveness" or request.path == "/api/healthcheck/liveness/":
            return JsonResponse({"message": "Ok"})

        return self.get_response(request)
