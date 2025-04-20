from django.urls import path
from .views import NameView

urlpatterns = [
    path("", NameView.as_view(), name="index"),
]
