from django.urls import path
from .views import YoutubeDownloader

urlpatterns = [path("", YoutubeDownloader.as_view(), name="youtube-downloader")]
