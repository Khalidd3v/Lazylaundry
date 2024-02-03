from django.urls import path
from . import views
urlpatterns = [
    path("signup-user", views.signup_user, name="signup_user")
]
