from swapper import load_model

from txn_notifications.base.admin import (
    AbstractCategoryAdmin,
    AbstractTemplateAdmin,
    AbstractNotificationAdmin,
)

from django.contrib import admin

Category = load_model("txn_notifications", "Category")
Template = load_model("txn_notifications", "Template")
Notification = load_model("txn_notifications", "Notification")


@admin.register(Category)
class CategoryAdmin(AbstractCategoryAdmin):
    pass


@admin.register(Template)
class TempalteAdmin(AbstractTemplateAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(AbstractNotificationAdmin):
    pass
