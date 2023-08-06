from django.test import TestCase

from swapper import load_model

from txn_notifications.tests.factories import (
    UserFactory,
    ReadNotification,
    NotificationFactory,
    SentNotificationFactory,
)

Notification = load_model("txn_notifications", "Notification")


class NotificationQSTestCase(TestCase):
    def setUp(self):
        NotificationFactory()
        NotificationFactory()
        SentNotificationFactory()
        SentNotificationFactory()
        SentNotificationFactory()
        ReadNotification()

    def test_filter_sent(self):
        self.assertEqual(Notification.objects.sent().count(), 3)

    def test_filter_unsent(self):
        self.assertEqual(Notification.objects.unsent().count(), 3)

    def test_filter_unread(self):
        self.assertEqual(Notification.objects.unread().count(), 5)

    def test_filter_read(self):
        self.assertEqual(Notification.objects.read().count(), 1)


class UserNotificationQSTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

        NotificationFactory(recipient=self.user)
        NotificationFactory(recipient=self.user)
        SentNotificationFactory(recipient=self.user)
        SentNotificationFactory(recipient=self.user)
        SentNotificationFactory(recipient=self.user)
        ReadNotification(recipient=self.user)

        # other notifications
        NotificationFactory()
        NotificationFactory()
        SentNotificationFactory()
        SentNotificationFactory()
        SentNotificationFactory()
        ReadNotification()

    def test_no_filter(self):
        self.assertEqual(self.user.notifications.count(), 6)

    def test_filter_read(self):
        self.assertEqual(self.user.notifications.read().count(), 1)

    def test_filter_unread(self):
        self.assertEqual(self.user.notifications.unread().count(), 5)

    def test_filter_sent(self):
        self.assertEqual(self.user.notifications.sent().count(), 3)

    def test_filter_unsent(self):
        self.assertEqual(self.user.notifications.unsent().count(), 3)

    def test_mark_all_as_read(self):
        self.assertEqual(self.user.notifications.read().count(), 1)
        Notification.objects.mark_all_as_read(recipient=self.user)
        self.assertEqual(self.user.notifications.unread().count(), 0)

    def test_mark_all_as_unread(self):
        self.assertEqual(self.user.notifications.unread().count(), 5)
        Notification.objects.mark_all_as_unread(recipient=self.user)
        self.assertEqual(self.user.notifications.read().count(), 0)

    def test_mark_all_as_sent(self):
        self.assertEqual(self.user.notifications.sent().count(), 3)
        Notification.objects.mark_all_as_sent(recipient=self.user)
        self.assertEqual(self.user.notifications.unsent().count(), 0)

    def test_mark_all_as_unsent(self):
        self.assertEqual(self.user.notifications.unsent().count(), 3)
        Notification.objects.mark_all_as_unsent(recipient=self.user)
        self.assertEqual(self.user.notifications.sent().count(), 0)
