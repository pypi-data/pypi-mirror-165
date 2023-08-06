from swapper import swappable_setting

from txn_notifications.base.models import (
    AbstractCategory,
    AbstractTemplate,
    AbstractNotification,
    AbstractUserHandlerSettings,
    AbstractUserCategorySettings,
)


class Category(AbstractCategory):
    class Meta(AbstractCategory.Meta):
        abstract = False
        swappable = swappable_setting("txn_notifications", "Category")


class Template(AbstractTemplate):
    class Meta(AbstractTemplate.Meta):
        abstract = False
        swappable = swappable_setting("txn_notifications", "Template")


class Notification(AbstractNotification):
    class Meta(AbstractNotification.Meta):
        abstract = False
        swappable = swappable_setting("txn_notifications", "Notification")


class UserCategorySettings(AbstractUserCategorySettings):
    class Meta(AbstractUserCategorySettings.Meta):
        abstract = False
        swappable = swappable_setting(
            "txn_notifications", "UserCategorySettings"
        )


class UserHandlerSettings(AbstractUserHandlerSettings):
    class Meta(AbstractUserHandlerSettings.Meta):
        abstract = False
        swappable = swappable_setting(
            "txn_notifications", "UserHandlerSettings"
        )
