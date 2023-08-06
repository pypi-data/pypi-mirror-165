from django.utils import timezone

import factory
from factory.django import DjangoModelFactory

from txn_notifications.models import (
    Category,
    Template,
    Notification,
    UserHandlerSettings,
    UserCategorySettings,
)

from django.contrib.auth import get_user_model


class UserFactory(DjangoModelFactory):
    first_name = factory.Faker("name")
    username = factory.Faker("email")
    email = factory.Faker("email")

    class Meta:
        model = get_user_model()


class CategoryFactory(DjangoModelFactory):
    name = factory.Faker("name")
    description = "category description"
    slug = factory.Faker("lexify", text="category_??????????")

    class Meta:
        model = Category


class TemplateFactory(DjangoModelFactory):
    name = factory.Faker("name")
    description = "template description"
    slug = factory.Faker("lexify", text="template_??????????__django")

    # turn on/off by category
    category = factory.SubFactory(CategoryFactory)

    # notification templates / regex
    title = "hi {{ recipient.first_name }}!"
    body = "this is a **mark_down** template"
    url = "https://app.test.mx/profile/{{ recipient.id }}/"
    url_msg = "See your profile"

    handler = "django"

    class Meta:
        model = Template


class NotificationFactory(DjangoModelFactory):
    recipient = factory.SubFactory(UserFactory)
    sender = factory.SubFactory(UserFactory)

    # in case a template have been used
    template = factory.SubFactory(TemplateFactory)

    title = "notification title"
    body = "notification body"
    url = "notification url"

    target = factory.SubFactory(UserFactory)

    class Meta:
        model = Notification


class SentNotificationFactory(NotificationFactory):
    sent = True
    sent_timestamp = timezone.now()

    prov_id = "123"
    prov_status = "sent"

    class Meta:
        model = Notification


class ReadNotification(NotificationFactory):
    read = True
    read_timestamp = timezone.now()

    class Meta:
        model = Notification


class UserCategorySettingsFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    allow = True

    class Meta:
        model = UserCategorySettings


class UserHandlerSettingFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    handler = "django"
    allow = True

    class Meta:
        model = UserHandlerSettings
