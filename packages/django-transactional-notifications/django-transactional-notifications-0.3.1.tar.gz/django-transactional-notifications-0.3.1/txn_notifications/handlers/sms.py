from django.conf import settings
from django.utils import timezone

from swapper import load_model
from twilio.rest import Client

from txn_notifications.exceptions import NotificationNotSent

from .generic import Handler

Notification = load_model("notification", "Notification")


class TwilioHandler(Handler):
    slug = "twilio"
    recipient_attr = None

    enabled = False
    sms_sender = None

    def __init__(self, *args, **kwargs):
        twilio = settings.DJANGO_NOTIFICATIONS.get("twilio")

        if not twilio.get("enabled", self.enabled):
            raise NotificationNotSent("twilio is not enabled.")

        self.recipient_attr = twilio.get("recipient_attr", self.recipient_attr)

        self.callback = twilio.get("callback", self.get_callback())

        self.__sms_sender = twilio.get("sms_sender", self.sms_sender)

        self.__client = Client(
            twilio.get("account_sid"), twilio.get("auth_token")
        )
        super().__init__(*args, **kwargs)

    def perform_send(self):
        sms_msg = self.get_sms_message()

        if self.template.check_status:
            if not self.callback:
                raise NotificationNotSent("no callback")

            # send notification to twilio (with callback)
            self.notification = self.__client.messages.create(
                to=self.recipient,
                from_=self.__sms_sender,
                body=sms_msg,
                status_callback=self.callback,
            )
        else:
            # send notification to twilio
            self.notification = self.__client.messages.create(
                to=self.recipient,
                from_=self.__sms_sender,
                body=sms_msg,
            )

    def get_sms_message(self):
        sms_msg = f"{self.title}"

        if self.body:
            sms_msg = f"{sms_msg} {self.body}"

        if self.url:
            if self.url_msg:
                sms_msg = f"{sms_msg} {self.url_msg} {self.url}"
            else:
                sms_msg = f"{sms_msg} {self.url}"

        return sms_msg

    @classmethod
    def get_prov_id(cls, response) -> str:
        """
        See Also:
            https://www.twilio.com/docs/sms/send-messages
        Args:
            response: Expected response when a message is sent:
                {
                  "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                  "api_version": "2010-04-01",
                  "body": "McAvoy or Stewart? These timelines can get so
                    confusing.",
                  "date_created": "Thu, 30 Jul 2015 20:12:31 +0000",
                  "date_sent": "Thu, 30 Jul 2015 20:12:33 +0000",
                  "date_updated": "Thu, 30 Jul 2015 20:12:33 +0000",
                  "direction": "outbound-api",
                  "error_code": null,
                  "error_message": null,
                  "from": "+15017122661",
                  "messaging_service_sid":
                    "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                  "num_media": "0",
                  "num_segments": "1",
                  "price": null,
                  "price_unit": null,
                  "sid": "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                  "status": "sent",
                  "subresource_uris": {
                    "media": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXX
                    XXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                    /Media.json"
                  },
                  "to": "+15558675310",
                  "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXX
                    XXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.json"
                }

        Returns:
            (str): response.data.sid
        """
        data = response.json()
        return data.get("sid")

    @classmethod
    def get_prov_status(cls, response):
        """
        See Also:
            https://www.twilio.com/docs/sms/send-messages
            https://www.twilio.com/docs/sms/api/message-resource#message-status-values
        Args:
            response: Expected response when a message is sent:
                {
                  "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                  "api_version": "2010-04-01",
                  "body": "McAvoy or Stewart? These timelines can get so
                    confusing.",
                  "date_created": "Thu, 30 Jul 2015 20:12:31 +0000",
                  "date_sent": "Thu, 30 Jul 2015 20:12:33 +0000",
                  "date_updated": "Thu, 30 Jul 2015 20:12:33 +0000",
                  "direction": "outbound-api",
                  "error_code": null,
                  "error_message": null,
                  "from": "+15017122661",
                  "messaging_service_sid":
                    "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                  "num_media": "0",
                  "num_segments": "1",
                  "price": null,
                  "price_unit": null,
                  "sid": "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                  "status": "sent",
                  "subresource_uris": {
                    "media": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXX
                    XXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                    /Media.json"
                  },
                  "to": "+15558675310",
                  "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXX
                    XXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.json"
                }

        Returns:
            ([str, str]): response.data.status, response.data.error_code
        """
        data = response.json()
        return data.get("status"), data.get("error_code")

    @classmethod
    def update_status(cls, response, callback_id=None):
        """

        Args:
            response:
            callback_id:

        See Also:
            # https://www.twilio.com/docs/sms/api/message-resource#message-status-values

        Returns:

        """
        notification = Notification.objects.get(callback_id=callback_id)

        status, error_code = cls.get_prov_status(response)

        if not notification.is_sent:
            notification.is_sent = status == "sent"
            if notification.is_sent:
                notification.sent_timestamp = timezone.now()

        if error_code:
            notification.data["error_code"] = error_code

        notification.status = status
        notification.save()
