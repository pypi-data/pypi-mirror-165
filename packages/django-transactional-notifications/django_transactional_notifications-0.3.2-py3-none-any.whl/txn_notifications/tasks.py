from django.utils import timezone

from swapper import get_model_name
from dateutil.relativedelta import relativedelta


def remove_old_notifications(time_ago=None):
    Notification = get_model_name("txn_notifications", "Notification")

    if not time_ago:
        time_ago = relativedelta(months=6)
    six_moths_ago = timezone.now() - time_ago
    Notification.objects.filter(created_timestamp__lte=six_moths_ago).delete()
