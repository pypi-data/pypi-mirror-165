from django.contrib import admin


class AbstractCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "name", "is_active"]
    list_filter = ["created_timestamp", "is_active"]
    search_fields = ["slug", "name"]
    readonly_fields = ["created_timestamp"]


class AbstractTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "name",
        "category",
        "title",
        "is_active",
    )
    list_filter = ["created_timestamp", "is_active"]
    search_fields = ["slug", "name"]
    readonly_fields = ["created_timestamp"]
    autocomplete_fields = ["category"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")


class AbstractNotificationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "recipient",
        "title",
        "read",
        "sent",
        "created_timestamp",
    ]
    list_filter = ["created_timestamp", "read", "sent"]
    search_fields = ["recipient__username", "recipient__first_name"]
    readonly_fields = [
        "created_timestamp",
        "recipient",
        "sender",
        "template",
        "target_content_type",
        "target_object_id",
        "sent",
        "sent_timestamp",
        "read",
        "read_timestamp",
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("recipient")
