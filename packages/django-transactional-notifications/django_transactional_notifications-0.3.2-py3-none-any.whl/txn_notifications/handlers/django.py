from django.utils import timezone

from swapper import load_model

from .generic import Handler


class DjangoHandler(Handler):
    slug = "django"
    recipient_attr = None  # uses self.user

    def send(self):
        Notification = load_model("txn_notifications", "Notification")

        recipient = self.get_recipient()
        self.notification = Notification.objects.create(
            recipient=recipient,
            sender=self.sender,
            template=self.template,
            title=self.title,
            body=self.body,
            url=self.url,
            url_msg=self.url_msg,
            sent=True,
            sent_timestamp=timezone.now(),
        )

    def post_send(self, response):
        pass  # recorded on send()

    def record_notification(self):
        pass  # recorded on send()

    def get_recipient(self):
        return self.user
