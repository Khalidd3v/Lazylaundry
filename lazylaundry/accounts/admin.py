from django.contrib import admin
from .models import *


# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
        "date_joined",
        "last_login",
        "first_name",
    )
    search_fields = ("email", "username")
    readonly_fields = ("id", "date_joined", "last_login", "password")


admin.site.register(LazyUser, AccountAdmin)