from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/",include('app.urls'), name="dashboard"),
    path("accounts/", include('accounts.urls'), name="accounts")
]
