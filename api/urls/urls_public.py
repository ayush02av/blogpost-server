from django.urls import path
from api.views import views_public

urlpatterns = [
    path("blogs/", views_public.blogs.as_view(), name="public_blogs"),
]