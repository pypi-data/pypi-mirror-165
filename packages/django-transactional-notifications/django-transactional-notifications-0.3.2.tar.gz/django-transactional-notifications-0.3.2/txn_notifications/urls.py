from django.urls import path

from .views import callbacks, generic_callbacks

urlpatterns = [
    path(
        "callbacks/<str:handler>/<uuid:callback_id>/",
        callbacks,
        name="notifications-callback",
    ),
    path(
        "callbacks/<str:handler>/",
        generic_callbacks,
        name="notifications-callback-generic",
    ),
]
