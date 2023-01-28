from django.urls import path
from api.views import views_auth

urlpatterns = [
    path("signup/", views_auth.signup_user.as_view(), name="auth_signup"),
    path("login/", views_auth.login_user.as_view(), name="auth_login"),
]
