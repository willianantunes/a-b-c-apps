from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

from letter_b.apps.example.api.v1 import views as views_v1

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    # The liveness endpoint is configured at letter_b/support/middlewares.py
    path("api/healthcheck/", include("health_check.urls"), name="health-check"),
    path("api/v1/users/attributes", views_v1.UserManagementAttributesAPIView.as_view()),
]

if settings.DEBUG and settings.USE_DEBUG_APPS:
    urlpatterns += [
        path("debug-toolbar/", include("debug_toolbar.urls")),  # django debug toolbar
    ]
