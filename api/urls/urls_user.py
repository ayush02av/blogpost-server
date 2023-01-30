from django.urls import path
from api.views import views_user

urlpatterns = [
    path("profile/", views_user.profile.as_view(), name="profile"),
    path("blog/", views_user.blogs.as_view(), name="user_blogs"),
    path("blog/<int:pk>", views_user.blog.as_view(), name="user_blog"),
    path("reset_password/", views_user.reset_password.as_view(), name="reset_password"),
]