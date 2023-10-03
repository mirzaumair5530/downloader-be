from django.urls import path
from .views import InstaDownloader

urlpatterns = [path("", InstaDownloader.as_view(), name="insta-downloader")]
