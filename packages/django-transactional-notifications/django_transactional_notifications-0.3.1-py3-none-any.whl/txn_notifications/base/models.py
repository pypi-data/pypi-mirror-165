import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone

import swapper

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class AbstractCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, db_index=True)

    is_active = models.BooleanField(default=True)

    created_timestamp = models.DateTimeField(default=timezone.now)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        abstract = True

    def __str__(self):
        return f"[{self.slug}] {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name

        super().save(*args, **kwargs)


class AbstractTemplate(models.Model):
    """
    Multiple templates for multiple handlers

    Templote(slug="welcome__mobile")
    """

    # template data
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, db_index=True)

    # turn on/off by category
    category = models.ForeignKey(
        swapper.get_model_name("txn_notifications", "Category"),
        on_delete=models.SET_NULL,
        related_name="templates",
        null=True,
    )

    # notification templates / markdown
    title = models.CharField(
        "Notification title",
        max_length=500,
        null=True,
        blank=True,
        help_text="Markdown and django template language enabled. "
        "You can use {{ <data> }}, for example: {{ recipient }}, "
        "{{ sender }}, {{ target }}.",
    )

    body = models.TextField(
        "Notification body",
        null=True,
        blank=True,
        help_text="Markdown and django template language enabled. "
        "You can use {{ <data> }}, for example: {{ recipient }}, "
        "{{ sender }}, {{ target }}.",
    )

    url = models.TextField(
        "Notification url",
        max_length=500,
        null=True,
        blank=True,
        help_text="Markdown and django template language enabled. "
        "You can use {{ <data> }}, for example: {{ recipient }}, "
        "{{ sender }}, {{ target }}.",
    )

    url_msg = models.TextField(
        "Notification url message",
        max_length=500,
        null=True,
        blank=True,
        help_text="Markdown and django template language enabled. "
        "You can use {{ <data> }}, for example: {{ recipient }}, "
        "{{ sender }}, {{ target }}.",
    )

    handler = models.CharField(max_length=50, help_text="handler slug")
    record = models.BooleanField(
        default=True,
        help_text="record the notification in the database using "
        "`Notification` model.",
    )

    check_status = models.BooleanField(
        default=True,
        help_text="check that the notification must update sent status, "
        "usually using callbacks or webhooks.",
    )

    # notifications can be sent using this template
    is_active = models.BooleanField(
        default=True,
        help_text="if `False`, avoid sending any notification using this "
        "template.",
    )

    created_timestamp = models.DateTimeField(default=timezone.now)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{self.name}__{self.handler}"

        if self.check_status:
            self.record = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"
        abstract = True

    def __str__(self):
        return f"[{self.slug}] {self.name}"


class NotificationQuerySet(models.query.QuerySet):
    def read(self):
        return self.filter(read=True)

    def unread(self):
        return self.filter(read=False)

    def sent(self):
        return self.filter(sent=True)

    def unsent(self):
        return self.filter(sent=False)

    def mark_all_as_read(self, recipient):
        """Mark as read all notifications for the current recipient."""
        self.unread().filter(recipient=recipient).update(read=True)

    def mark_all_as_unread(self, recipient):
        """Mark as unread all notifications for the current recipient."""
        self.read().filter(recipient=recipient).update(read=False)

    def mark_all_as_sent(self, recipient):
        """Mark as sent all notifications for the current recipient."""
        self.unsent().filter(recipient=recipient).update(sent=True)

    def mark_all_as_unsent(self, recipient):
        """Mark as read unsent all notifications for the current recipient."""
        self.sent().filter(recipient=recipient).update(sent=False)


class AbstractNotification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notifications",
        on_delete=models.CASCADE,
        blank=False,
        db_index=True,
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_notifications",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    # in case a template have been used
    template = models.ForeignKey(
        swapper.get_model_name("txn_notifications", "Template"),
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(max_length=200)
    body = models.TextField(
        null=True,
        blank=True,
    )

    # the main call to action url
    url = models.CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    url_msg = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    # extra context data
    data = models.JSONField(null=True)

    # for handlers that can mark as read
    read = models.BooleanField(
        default=False, help_text="Notification has been read for the user?"
    )
    read_timestamp = models.DateTimeField(null=True, blank=True)

    # for handlers that must check that the notification has been sent using
    # webhooks
    sent = models.BooleanField(
        default=False,
        help_text="Notification has been confirmed sent to the user?",
    )
    sent_timestamp = models.DateTimeField(null=True, blank=True)

    prov_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Provider's notification id",
    )
    prov_status = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Provider's internal status",
    )

    # object related to the notification
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = GenericForeignKey("target_content_type", "target_object_id")

    created_timestamp = models.DateTimeField(default=timezone.now)

    callback_id = models.UUIDField(default=uuid.uuid4, editable=False)

    objects = NotificationQuerySet.as_manager()

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        abstract = True
        ordering = ("-created_timestamp",)

    def __str__(self):
        return f"{self.recipient} {self.title} {self.timesince()} ago"

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_

        return timesince_(self.created_timestamp, now)

    def mark_as_read(self):
        if not self.read:
            self.read = True
            self.read_timestamp = timezone.now()
            self.save()
        return self.read

    def mark_as_unread(self):
        if self.read:
            self.read = False
            self.save()
        return self.read

    def mark_as_sent(self):
        if not self.sent:
            self.sent = True
            self.sent_timestamp = timezone.now()
            self.save()
        return self.sent


class AbstractUserHandlerSettings(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notify_handler_settings",
        on_delete=models.CASCADE,
        db_index=True,
    )
    handler = models.CharField(max_length=50)
    allow = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User handler settings"
        verbose_name_plural = "User handler settings"
        unique_together = ("user", "handler")
        abstract = True


class AbstractUserCategorySettings(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notify_category_settings",
        db_index=True,
    )
    category = models.ForeignKey(
        swapper.get_model_name("txn_notifications", "Category"),
        on_delete=models.CASCADE,
    )
    allow = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User category settings"
        verbose_name_plural = "User category settings"
        unique_together = ("user", "category")
        abstract = True
