from django.urls import path, include

urlpatterns = [
    path("auth/", include('api.urls.urls_auth')),
    path("user/", include('api.urls.urls_user')),
]
