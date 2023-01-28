from django.urls import path
from .views import views_user

urlpatterns = [
    path("auth/signup/", views_user.signup_user.as_view(), name="auth_signup"),
]
