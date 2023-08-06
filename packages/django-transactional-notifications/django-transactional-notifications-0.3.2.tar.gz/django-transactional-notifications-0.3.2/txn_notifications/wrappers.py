from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from swapper import load_model

from .exceptions import (
    WrapperError,
    HandlerDisallowed,
    CategoryDisallowed,
    NotificationNotSent,
)

Template = load_model("txn_notifications", "Template")


error_msgs = {
    # wrapper
    "no_handlers": "`supported_handlers` is required.",
    "no_active_handlers": "No supported handlers.",
    "no_active_template": "No active templates for this notification.",
    "missing_defaults": "`template_name`, `template_slug` and `title` are "
    "required attributes",
    # user
    "no_active_rcpt": "`recipient` is not an active user.",
    "disallowed_category": "The recipient didn't allowed notifications from "
    "this category.",
    "disallowed_handler": "The recipient didn't allowed notifications from "
    "this handler.",
}


class NotificationWrapper:
    """
    Creates templates and send notifications.
    """

    # template
    template_name = None  # required
    template_description = None
    template_slug = None  # required & unique
    template_category = None

    # default notification template
    title = None  # required
    body = None
    url = None
    url_msg = None
    is_active = True

    supported_handlers = []

    def __init__(self):
        if not self.supported_handlers:
            raise WrapperError(
                error_msgs["no_handlers"],
                code="no_handlers",
            )

        handler_slugs = [handler.slug for handler in self.supported_handlers]

        self.templates = Template.objects.filter(
            Q(slug__startswith=f"{self.template_slug}__")
            & Q(is_active=True)
            & Q(handler__in=handler_slugs)
            & Q(Q(category__isnull=True) | Q(category__is_active=True))
        )

        if not self.templates.exists():
            raise WrapperError(
                error_msgs["no_active_template"], code="no_active_template"
            )

    def send(
        self, recipient, *, sender=None, target=None, data=None, context=None
    ) -> None:
        """
        Send all the notification using all supported handlers.

        Args:
            recipient (User): Recipient of the notification.
            sender (User): User who sends the notification.
            target: Any django model to wich the notification is related.
            data (dict): Optional. Any data visible to the wrapper and the
                handler. Accesible to the templates.
            context (dict): Optional. Any context visible to the wrapper and
                the handlers

        Raises:
            NotificationNotSent: if the notification is not sent.
        """
        # check that user allow notifications
        self._check_recipient(recipient)

        # adding context
        data = self.get_data(
            data=data,
            recipient=recipient,
            sender=sender,
            target=target,
            context=context,
        )

        for template in self.templates:
            self._send_notification(template, recipient, sender, target, data)

    def send_notification(
        self,
        template_slug,
        recipient,
        *,
        sender=None,
        target=None,
        data=None,
        context=None,
    ):
        """
        Sends a notification using a template, without using send().

        Args:
            template_slug (str): template real slug.
                f.e. {template_slug}__{handler_slug}
            recipient (User):
            sender (User):
            target:
            data (dict):
            context (dict):

        Examples:
            >>> # send the email notfication only
            >>> send_notification("new_announcement__email", *args, **kwargs)
        """
        self._check_recipient(recipient)
        data = self.get_data(
            data=data,
            recipient=recipient,
            sender=sender,
            target=target,
            context=context,
        )

        try:
            # expected template__handler format
            template = self.templates.get(slug=template_slug)

        except ObjectDoesNotExist as e:
            raise WrapperError(
                error_msgs["no_active_template"], code="no_active_template"
            ) from e
        self._send_notification(
            template,
            recipient,
            sender,
            target,
            data,
        )

    def _send_notification(
        self,
        template,
        recipient,
        sender=None,
        target=None,
        data=None,
    ):
        try:
            # check user settings
            self._check_recipient_settings(recipient, template)

            data["template"] = template
            HandlerClass = self.get_handler(template)
            handler = HandlerClass(
                recipient, template, sender=sender, data=data
            )
            handler.send()
        except Exception as e:
            self.hadle_exception(e, template, recipient, sender, target, data)

    def hadle_exception(
        self,
        exception,
        template,
        recipient,
        sender=None,
        target=None,
        data=None,
    ):
        raise exception

    @classmethod
    def get_data(
        cls,
        *,
        data=None,
        recipient=None,
        sender=None,
        target=None,
        context=None,
        **kwargs,
    ):
        data = data or {}
        data.update(
            {
                "recipient": recipient,
                "sender": sender,
                "target": target,
                "template": None,  # added latter on the send function.
                "context": context or {},
            }
        )
        return data

    # ==========================================
    # recipient
    # ==========================================
    @classmethod
    def _check_recipient(cls, recipient):
        """

        Args:
            recipient:

        Returns:

        """
        if not recipient.is_active:
            raise NotificationNotSent(
                error_msgs["no_active_rcpt"], code="no_active_rcpt"
            )

    @classmethod
    def _check_recipient_settings(cls, user, template):
        """

        Args:
            user:
            template:

        Returns:

        """
        if user.notify_handler_settings.filter(
            handler=template.handler, allow=False
        ).exists():
            raise HandlerDisallowed(
                error_msgs["disallowed_handler"],
                code="disallowed_handler",
            )

        if template.category:
            if user.notify_category_settings.filter(
                category=template.category,
                allow=False,
            ).exists():
                raise CategoryDisallowed(
                    error_msgs["disallowed_category"],
                    code="disallowed_category",
                )

    # ==========================================
    # Wrapper
    # ==========================================
    @classmethod
    def _check_validate_defaults(cls):
        if (
            cls.template_name is None
            or cls.template_slug is None
            or cls.title is None
        ):
            raise WrapperError(
                error_msgs["missing_defaults"], code="missing_defaults"
            )

    @classmethod
    def get_handler(cls, template):
        for handler in cls.supported_handlers:
            if handler.slug == template.handler:
                return handler

        raise WrapperError(
            error_msgs["no_active_handlers"], code="no_active_handlers"
        )

    @classmethod
    def _get_category(cls):
        if cls.template_category:
            Category = load_model("txn_notifications", "Category")
            return Category.objects.get(slug=cls.template_category)
        return None

    # ==========================================
    # templates
    # ==========================================
    @classmethod
    def create_templates(cls, update_existing=False):
        """
        Creates or update templates.
        It will create a template for every template-handler combination.
        template_slug = f"{template_slug}__{handler.slug}"

        Args:
            update_existing (bool): Must update existing templates?
        """
        cls._check_validate_defaults()

        for handler in cls.supported_handlers:
            template = Template.objects.filter(
                slug=cls.get_template_slug(handler),
                handler=handler.slug,
            ).first()

            if not template:
                cls._create_template(handler)
            elif update_existing:
                cls._update_template(template, handler)

    @classmethod
    def _create_template(cls, handler) -> None:
        """Creates a new template.
        Uses {handler}_{attribute} combination to set the attrbitures or
        default data.

        Args:
            handler (Handler):
        """
        Template.objects.create(
            slug=cls.get_template_slug(handler),
            name=cls.template_name,
            description=cls.template_description,
            handler=handler.slug,
            category=cls._get_category(),
            title=getattr(
                cls,
                f"{handler.slug}_title",
                cls.title,
            ),
            body=getattr(
                cls,
                f"{handler.slug}_body",
                cls.body,
            ),
            url=getattr(
                cls,
                f"{handler.slug}_url",
                cls.url,
            ),
            url_msg=getattr(cls, f"{handler.slug}_url_msg", cls.url_msg),
            is_active=getattr(
                cls,
                f"{handler.slug}_is_active",
                cls.is_active,
            ),
        )

    @classmethod
    def _update_template(cls, template, handler) -> None:
        """
        Updates templates if `update_existing` flag is True on
        `create_templates` function.

        Args:
            template (Template):
            handler (Hander):

        Returns:
            None
        """
        template.name = cls.template_name
        template.description = cls.template_description
        template.category = cls._get_category()

        # uses the handler related attributes or the default attributes.
        template.title = getattr(
            cls,
            f"{handler.slug}_title",
            cls.title,
        )
        template.body = getattr(
            cls,
            f"{handler.slug}_body",
            cls.body,
        )
        template.url = getattr(
            cls,
            f"{handler.slug}_url",
            cls.url,
        )
        template.is_active = getattr(
            cls,
            f"{handler.slug}_is_active",
            cls.is_active,
        )
        template.save()

    @classmethod
    def get_template_slug(cls, handler):
        return f"{cls.template_slug}__{handler.slug}"
