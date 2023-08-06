from django.template import Context
from django.template import Template as DjangoTemplate

from swapper import load_model

from txn_notifications.settings import get_settings
from txn_notifications.exceptions import NotificationNotSent

settings = get_settings()


class Handler:
    slug = None
    recipient_attr = None

    check_status = None
    record = None

    def __init__(
        self,
        recipient,
        template,
        *,
        sender=None,
        data=None,
        **kwargs,
    ):
        if not self.slug:
            raise NotificationNotSent("handler must have a slug.")

        if not settings.get(self.slug):
            raise NotificationNotSent(
                f"handler '{self.slug}' setttings are required."
            )

        self.recipient_attr = settings.get(self.slug).get("recipient_attr")

        self.user = recipient  # User object
        self.template = template
        self.sender = sender
        self.data = data
        self.context = data.get("context", {})

        # prepare the message to the provider
        self.title = self.get_title()
        self.body = self.get_body()
        self.url = self.get_url()
        self.url_msg = self.get_url_msg()

        self.data["title"] = self.title
        self.data["body"] = self.body
        self.data["url"] = self.url
        self.data["url_msg"] = self.url_msg

        # gets the string recipient to send it to the provider.
        # For example: for an email it migth be user.email
        self.recipient = self.get_recipient()
        self.data["recipient_attr"] = self.recipient

        self.notification = None

    def pre_send(self) -> None:
        """
        Data formating and additional validations.
        """

    def send(self) -> None:
        """
        Prepares, sends and saves the notification info.
        """
        self.pre_send()
        response = self.perform_send()
        self.post_send(response)

    def perform_send(self) -> object:
        """
        Send the notification to the provider.

        Returns:
            Provider's http response
        """
        raise NotImplementedError()

    def post_send(self, response) -> None:

        if self.record is not None and not self.record:
            pass
        elif self.template.record:
            # record on the database
            # populate self.notification
            self.record_notification()

        if self.check_status is not None and not self.check_status:
            pass
        elif self.template.check_status:
            self.notification.prov_id = self.get_prov_id(response)
            self.notification.prov_status = self.get_prov_status(response)
            self.notification.save()

    def record_notification(self):
        Notification = load_model("txn_notifications", "Notification")
        self.notification = Notification.objects.create(
            recipient=self.user,
            sender=self.sender,
            template=self.template,
            title=self.title,
            body=self.body,
            url=self.url,
            url_msg=self.url_msg,
        )

    def get_title(self) -> str:
        """
        Renders the title.
        Returns:
            (str): The title rendered.
        """
        context = Context(self.data)
        template = DjangoTemplate(self.template.title)
        return template.render(context)

    def get_body(self) -> str:
        """
        Renders the body.
        Returns:
            (str): The body rendered or empty string if is None.
        """
        if not self.template.body:
            return ""

        context = Context(self.data)
        template = DjangoTemplate(self.template.body)
        return template.render(context)

    def get_url(self) -> str:
        """
        Renders the url.
        Returns:
            (str): The url rendered or empty string if is None.
        """
        if not self.template.url:
            return ""

        context = Context(self.data)
        template = DjangoTemplate(self.template.url)
        return template.render(context)

    def get_url_msg(self) -> str:
        """
        Renders the url message.
        Returns:
            (str): The url message rendered or empty string if is None.
        """
        if not self.template.url_msg:
            return ""

        context = Context(self.data)
        template = DjangoTemplate(self.template.url_msg)
        return template.render(context)

    def get_recipient(self) -> str:
        """
        Get the recipient string to use it into the provider.

        Returns:
            (str): The recipient for the provider.

        Raises:
            NotificationNotSent if the attribute is not found or is empty
        """
        recipient = getattr(self.user, self.recipient_attr)
        if not recipient:
            raise NotificationNotSent(
                f"Recipient don't have {self.recipient_attr} attribute."
            )
        return recipient

    """
    Status
    """

    def get_callback(self) -> str:
        """ """
        from django.urls import reverse

        return reverse(
            "notifications-callback", args=[self.notification.callback_id]
        )

    @classmethod
    def get_prov_id(cls, request) -> str:
        """
        Gets the provider's id from the response.

        Args:
            request: HTTPResponse after sending the notification to the
            provider.
        """
        raise NotImplementedError()

    @classmethod
    def get_prov_status(cls, request) -> str:
        """
        Gets the provider's status from the response.

        Args:
            request: HTTPResponse after sending the notification to the
            provider.
        """
        # use any provider
        raise NotImplementedError()

    @classmethod
    def update_status(cls, request, callback_id=None):
        """

        Args:
            callback_id: Notification callback_id
            request: HTTPRequest from the provider's callback
        """
        raise NotImplementedError("update status must be implemented.")
