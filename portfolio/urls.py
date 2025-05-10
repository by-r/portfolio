from django.urls import path

from .views import NameView, ProfileView

urlpatterns = [
    path("", NameView.as_view(), name="index"),
    path("test/", ProfileView.as_view(), name="profile"),
]
