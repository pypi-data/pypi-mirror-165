from django.urls import path

from django.contrib import admin

urlpatterns = [
    # admin
    path("admin/", admin.site.urls)
]
