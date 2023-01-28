from django.urls import path
from api.views import views_user

urlpatterns = [
    path("profile/", views_user.profile.as_view(), name="profile"),
    path("logout/", views_user.logout_user.as_view(), name="logout"),
]
