from django.test import TestCase

from txn_notifications.tests.factories import UserFactory, TemplateFactory


class TemplateTestCase(TestCase):
    def setUp(self):
        self.recipient = UserFactory()
        self.template = TemplateFactory(
            title="{{ recipient.first_name }} **markdown**",
            body="{{ recipient.first_name }} **markdown**",
            url="{{ recipient.first_name }} **markdown**",
            url_msg="{{ recipient.first_name }} **markdown**",
        )
