"""
Templates based on https://github.com/mailgun/transactional-email-templates
"""
from django.conf import settings as django_settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from txn_notifications.settings import get_settings

from .generic import Handler

settings = get_settings()
email_settings = settings.get("email")
TXT_TEMPLATE = email_settings.get("txt_template")
HTML_TEMPLATE = email_settings.get("html_template")


class EmailHandler(Handler):
    slug = "email"
    recipient_attr = "email"

    check_status = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = None

    def pre_send(self) -> None:
        self.email = EmailMultiAlternatives(
            subject=self.title,
            body=self.get_txt_body(),
            from_email=self.get_from_email(),
            to=self.recipient,
            bcc=self.data.get("bcc"),
            connection=self.data.get("connection"),
            attachments=self.data.get("attachments"),
            headers=self.data.get("headers"),
            alternatives=self.data.get("alternatives"),
            cc=self.data.get("cc"),
            reply_to=self.data.get("reply_to"),
        )

        self.email.attach_alternative(self.get_html_body(), "text/html")

    def perform_send(self):
        return self.email.send()

    def get_recipient(self) -> list[str]:
        if type(self.user) == list:
            return [getattr(user, self.recipient_attr) for user in self.user]
        return [getattr(self.user, self.recipient_attr)]

    def get_from_email(self):
        return self.data.get("from_email", django_settings.DEFAULT_FROM_EMAIL)

    def get_txt_body(self):
        template = self.context.get("txt_template", TXT_TEMPLATE)
        return render_to_string(template, self.data)

    def get_html_body(self):
        template = self.context.get("html_template", HTML_TEMPLATE)
        return render_to_string(template, self.data)


class MailgunHandler(EmailHandler):
    @classmethod
    def get_prov_id(cls, request) -> str:
        """

        https://documentation.mailgun.com/en/latest/user_manual.html#sending-via-api
        {
          "message": "Queued. Thank you.",
          "id": "<20111114174239.25659.5817@samples.mailgun.org>"
        }

        Args:
            request:

        Returns:

        """
        data = request.json()
        return data.get("id")

    @classmethod
    def get_prov_status(cls, request) -> str:
        return ""

    @classmethod
    def update_status(cls, request, callback_id=None):
        """
        https://documentation.mailgun.com/en/latest/user_manual.html#webhooks-1

        Args:
            callback_id:
            request:

        Returns:

        """

    @classmethod
    def _verify(cls, signing_key, token, timestamp, signature):
        """
        To verify the webhook is originating from Mailgun you need to:

        * Concatenate timestamp and token values.
        * Encode the resulting string with the HMAC algorithm (using your
            Webhook Signing Key as a key and SHA256 digest mode).
        * Compare the resulting hexdigest to the signature.
        * Optionally, you can cache the token value locally and not honor
            any subsequent request with the same token. This will prevent
            replay attacks.
        * Optionally, you can check if the timestamp is not too far from the
        current time.

        https://www.mailgun.com/blog/email/your-guide-to-webhooks/

        Args:
            signing_key:
            token:
            timestamp:
            signature:

        Returns:

        """
        import hmac
        import hashlib

        hmac_digest = hmac.new(
            key=signing_key.encode(),
            msg=f"{timestamp}{token}".encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(str(signature), str(hmac_digest))
