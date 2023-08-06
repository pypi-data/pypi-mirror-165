import os

from django.conf import settings

from txn_notifications.templates import BASE_DIR

DEFAULTS = {
    "django": {
        "enabled": False,
    },
    "email": {
        "enabled": False,
        # default options
        "html_template": os.path.join(
            BASE_DIR, "txn_notifications/templates/email.html"
        ),
        "txt_template": os.path.join(
            BASE_DIR, "txn_notifications/templates/email.txt"
        ),
        # how to get the recipient
        "recipient_attr": "email",
    },
    "twilio": {
        # twilio handler is enabled
        "enabled": False,
        # account settings
        "account_sid": None,
        "auth_token": None,
        "sms_sender": None,
        # how to get the recipient
        "recipient_attr": None,
    },
}


def get_settings():
    user_settings = settings.DJANGO_NOTIFICATIONS
    custom_settings = DEFAULTS.copy()
    custom_settings.update(user_settings)
    return custom_settings
