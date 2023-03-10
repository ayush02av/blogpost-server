from django.urls import path
from api.views import views_public

urlpatterns = [
    path("blog/", views_public.blogs.as_view(), name="public_blogs"),
    path("blog/<int:id>/", views_public.blog.as_view(), name="public_blogs"),
]
