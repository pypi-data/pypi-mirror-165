from django.test import TestCase
from django.utils import timezone

from txn_notifications.tests.factories import NotificationFactory


class NotificationMarkTestCase(TestCase):
    def test_mark_as_read(self):
        notification = NotificationFactory(read=False, read_timestamp=None)

        self.assertFalse(notification.read)
        self.assertIsNone(notification.read_timestamp)

        notification.mark_as_read()

        self.assertTrue(notification.read)
        self.assertIsNotNone(notification.read_timestamp)

    def test_mark_as_unread(self):
        notification = NotificationFactory(
            read=True, read_timestamp=timezone.now()
        )

        self.assertTrue(notification.read)
        self.assertIsNotNone(notification.read_timestamp)

        notification.mark_as_unread()

        self.assertFalse(notification.read)
        self.assertIsNotNone(notification.read_timestamp)

    def test_mark_as_sent(self):
        notification = NotificationFactory(sent=False, sent_timestamp=None)

        self.assertFalse(notification.sent)
        self.assertIsNone(notification.sent_timestamp)

        notification.mark_as_sent()

        self.assertTrue(notification.sent)
        self.assertIsNotNone(notification.sent_timestamp)
