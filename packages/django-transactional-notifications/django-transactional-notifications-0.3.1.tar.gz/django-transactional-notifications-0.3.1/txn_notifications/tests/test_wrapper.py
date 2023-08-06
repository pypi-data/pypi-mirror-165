from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

import factory

from txn_notifications.models import Template
from txn_notifications.wrappers import NotificationWrapper
from txn_notifications.exceptions import (
    WrapperError,
    HandlerDisallowed,
    CategoryDisallowed,
    NotificationNotSent,
)
from txn_notifications.handlers.django import DjangoHandler
from txn_notifications.tests.factories import (
    UserFactory,
    CategoryFactory,
    TemplateFactory,
    UserHandlerSettingFactory,
    UserCategorySettingsFactory,
)


class NotificationWrapperTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(email=factory.Faker("email"))

    def setup_min_wrapper(self):
        class Wrapper(NotificationWrapper):
            template_name = "name"
            template_slug = "slug"
            title = "title"

            supported_handlers = [DjangoHandler]

        return Wrapper

    # ==========================================
    # send
    # ==========================================
    def test_send__min(self):
        Wrapper = self.setup_min_wrapper()

        Wrapper.create_templates()
        self.assertEqual(Template.objects.count(), 1)
        template = Template.objects.first()

        self.assertEqual(self.user.notifications.count(), 0)

        notification = Wrapper()
        notification.send(recipient=self.user)

        self.assertEqual(self.user.notifications.count(), 1)

        # check user notifications
        self.assertEqual(self.user.notifications.count(), 1)
        notification = self.user.notifications.first()

        # status
        self.assertFalse(notification.read)
        self.assertIsNone(notification.read_timestamp)
        self.assertTrue(notification.sent)
        self.assertIsNotNone(notification.sent_timestamp)

        # related
        self.assertIsNone(notification.sender)
        self.assertEqual(notification.template, template)
        self.assertEqual(notification.title, Wrapper.title)
        self.assertEqual(notification.body, "")
        self.assertEqual(notification.url, "")
        self.assertEqual(notification.url_msg, "")

    def test_send__sender(self):
        sender = UserFactory()

        Wrapper = self.setup_min_wrapper()

        Wrapper.create_templates()
        self.assertEqual(Template.objects.count(), 1)
        template = Template.objects.first()

        self.assertEqual(self.user.notifications.count(), 0)

        notification = Wrapper()
        notification.send(recipient=self.user, sender=sender)

        # check user notifications
        self.assertEqual(self.user.notifications.count(), 1)
        notification = self.user.notifications.first()

        # status
        self.assertFalse(notification.read)
        self.assertIsNone(notification.read_timestamp)
        self.assertTrue(notification.sent)
        self.assertIsNotNone(notification.sent_timestamp)

        # related
        self.assertEqual(notification.sender, sender)
        self.assertEqual(notification.template, template)
        self.assertEqual(notification.title, Wrapper.title)
        self.assertEqual(notification.body, "")
        self.assertEqual(notification.url, "")
        self.assertEqual(notification.url_msg, "")

    def test_send__data(self):
        pass

    def test_send__context(self):
        pass

    def test_send__no_templates(self):
        class Wrapper(NotificationWrapper):
            supported_handlers = [DjangoHandler]

        try:
            Wrapper().send(recipient=self.user)
            self.fail("WrapperException must be raised")
        except WrapperError as e:
            self.assertEqual(e.code, "no_active_template")

    # ==========================================
    # data context
    # ==========================================
    def test_get_default_data(self):
        sender = UserFactory()

        Wrapper = self.setup_min_wrapper()
        data = Wrapper.get_data(
            recipient=self.user, sender=sender, target=sender
        )
        self.assertEqual(data.get("recipient"), self.user)
        self.assertEqual(data.get("sender"), sender)
        self.assertEqual(data.get("target"), sender)

    def test_get_data__custom(self):
        sender_user = UserFactory()

        class Wrapper(NotificationWrapper):
            @classmethod
            def get_data(cls, *args, **kwargs):
                data = super().get_data(*args, **kwargs)
                data["foo"] = "bar"
                return data

        data = Wrapper.get_data(recipient=self.user, sender=sender_user)
        self.assertEqual(data.get("recipient"), self.user)
        self.assertEqual(data.get("sender"), sender_user)
        self.assertEqual(data.get("foo"), "bar")

    def test_get_handler(self):
        Wrapper = self.setup_min_wrapper()
        Wrapper.create_templates()
        template = Template.objects.first()

        handler = Wrapper.get_handler(template)
        self.assertEqual(handler, Wrapper.supported_handlers[0])

    def test_get_category(self):
        class Wrapper(NotificationWrapper):
            template_name = "name"
            template_slug = "slug"
            title = "title"

            template_category = "category"

        _category = CategoryFactory(name="category", slug="category")

        category = Wrapper._get_category()
        self.assertEqual(category.id, _category.id)
        self.assertEqual(category.slug, _category.slug)
        self.assertEqual(category.name, _category.name)

    def test_get_category__no_template_category(self):
        Wrapper = self.setup_min_wrapper()
        self.assertIsNone(Wrapper._get_category())

    def test_get_category__doesnt_exists(self):
        class Wrapper(NotificationWrapper):
            template_name = "name"
            template_slug = "slug"
            title = "title"

            template_category = "x"

        try:
            Wrapper._get_category()
            self.fail("expected ObjectDoesNotExist")
        except ObjectDoesNotExist:
            pass

    # ==========================================
    # templates
    # ==========================================
    def test_create_templates(self):
        Wrapper = self.setup_min_wrapper()

        self.assertEqual(Template.objects.count(), 0)
        Wrapper.create_templates()
        self.assertEqual(Template.objects.count(), 1)

        template = Template.objects.first()
        self.assertEqual(template.name, Wrapper.template_name)
        self.assertEqual(
            template.slug, Wrapper.get_template_slug(DjangoHandler)
        )
        self.assertEqual(template.title, Wrapper.title)
        self.assertEqual(template.handler, DjangoHandler.slug)
        self.assertIsNone(template.category)
        self.assertTrue(template.is_active)

    def test_create_templates__missing_defaults(self):
        class Wrapper(NotificationWrapper):
            supported_handlers = [DjangoHandler]

        try:
            Wrapper.create_templates()
        except WrapperError as e:
            self.assertEqual(e.code, "missing_defaults")

    def test_create_templates__no_handlers(self):
        class Wrapper(NotificationWrapper):
            supported_handlers = []

        try:
            Wrapper()
            self.fail("Wrapper exception must be raised")
        except WrapperError as e:
            self.assertEqual(e.code, "no_handlers")

    def test_create_templates__default_attributes(self):
        class Wrapper(NotificationWrapper):
            template_name = "name"
            template_slug = "slug"
            template_description = "description"

            title = "title"
            body = "body"
            url = "url"
            url_msg = "url_msg"
            is_active = True

            supported_handlers = [DjangoHandler]

        self.assertEqual(Template.objects.count(), 0)

        Wrapper.create_templates()

        self.assertEqual(Template.objects.count(), 1)
        template = Template.objects.first()

        self.assertEqual(
            template.slug, Wrapper.get_template_slug(DjangoHandler)
        )
        self.assertEqual(template.name, Wrapper.template_name)
        self.assertEqual(template.description, Wrapper.template_description)
        self.assertEqual(template.title, Wrapper.title)
        self.assertEqual(template.body, Wrapper.body)
        self.assertEqual(template.url, Wrapper.url)
        self.assertEqual(template.url_msg, Wrapper.url_msg)
        self.assertTrue(template.is_active)

    def test_create_templates__custom_attributes(self):
        class Wrapper(NotificationWrapper):
            template_name = "name"
            template_slug = "slug"
            template_description = "description"

            title = "title"
            body = "body"
            url = "url"
            url_msg = "url_msg"
            is_active = True

            django_title = "django title"
            django_body = "django body"
            django_url = "django url"
            django_url_msg = "django url msg"
            django_is_active = False

            supported_handlers = [DjangoHandler]

        self.assertEqual(Template.objects.count(), 0)

        Wrapper.create_templates()

        self.assertEqual(Template.objects.count(), 1)
        template = Template.objects.first()

        self.assertEqual(
            template.slug, Wrapper.get_template_slug(DjangoHandler)
        )
        self.assertEqual(template.name, Wrapper.template_name)
        self.assertEqual(template.description, Wrapper.template_description)
        self.assertEqual(template.title, Wrapper.django_title)
        self.assertEqual(template.body, Wrapper.django_body)
        self.assertEqual(template.url, Wrapper.django_url)
        self.assertEqual(template.url_msg, Wrapper.django_url_msg)
        self.assertEqual(template.is_active, Wrapper.django_is_active)

    def test_create_templates__category(self):
        category = CategoryFactory(name="Category name", slug="category")

        class Wrapper(NotificationWrapper):
            template_name = "name"
            template_slug = "slug"
            template_description = "description"
            template_category = category.slug

            title = "title"

            supported_handlers = [DjangoHandler]

        Wrapper.create_templates()

        self.assertEqual(Template.objects.count(), 1)
        template = Template.objects.first()
        self.assertEqual(template.category, category)

    def test_create_templates__no_category(self):
        class Wrapper(NotificationWrapper):
            template_name = "name"
            template_slug = "slug"
            template_description = "description"
            template_category = "xxx"

            title = "title"

            supported_handlers = [DjangoHandler]

        try:
            Wrapper.create_templates()
            self.fail("expected ObjectDoesNotExist")
        except ObjectDoesNotExist:
            pass

    def test_update_templates(self):
        pass

    def test_update_templates__default_attributes(self):
        pass

    def test_update_templates__custom_attributes(self):
        pass

    def test_update_templates__category(self):
        pass

    def test_update_templates__no_category(self):
        pass

    # ==========================================
    # check funcions
    # ==========================================
    def test_check_recipient(self):
        self.assertTrue(self.user.is_active)
        NotificationWrapper._check_recipient(self.user)

    def test_check_recipient__no_active(self):
        self.user.is_active = False
        self.user.save()

        try:
            NotificationWrapper._check_recipient(self.user)
            self.fail("NotificationNotSent should be raised")
        except NotificationNotSent as e:
            self.assertEqual(e.code, "no_active_rcpt")

    def test_check_recipient_settings_handler__allow(self):
        pass

    def test_check_recipient_settings_handler__disallow(self):
        settings = UserHandlerSettingFactory(
            handler=DjangoHandler.slug, allow=False
        )
        user = settings.user

        template = TemplateFactory(handler=DjangoHandler.slug)
        try:
            NotificationWrapper._check_recipient_settings(user, template)
            self.fail("HandlerDisallowed expected")
        except HandlerDisallowed as e:
            self.assertEqual(e.code, "disallowed_handler")

    def test_check_recipient_settings_category__allow(self):
        category = CategoryFactory()

        settings = UserCategorySettingsFactory(category=category, allow=True)
        user = settings.user

        template = TemplateFactory(category=category)
        self.assertEqual(settings.category, template.category)

        NotificationWrapper._check_recipient_settings(user, template)

    def test_check_recipient_settings_category__disallow(self):
        category = CategoryFactory()

        settings = UserCategorySettingsFactory(category=category, allow=False)
        user = settings.user

        template = TemplateFactory(category=category)
        try:
            NotificationWrapper._check_recipient_settings(user, template)
            self.fail("CategoryDisallowed expected")
        except CategoryDisallowed as e:
            self.assertEqual(e.code, "disallowed_category")
