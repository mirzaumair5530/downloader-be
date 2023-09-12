from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pytube import YouTube
import ssl

from .serializers import ResponseSerializer

ssl._create_default_https_context = ssl._create_stdlib_context


class PyTubeCustomError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class YoutubeDownloader(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):

        try:
            url = request.query_params.get("url")
            if not url:
                raise PyTubeCustomError("Please provide Url")
            yt = YouTube(url)

            urls = [
                {"quality": format["qualityLabel"], "url": format["url"]}
                for format in yt.streaming_data["formats"]
            ]

            serializer = ResponseSerializer(data=urls, many=True)

            if serializer.is_valid():
                return Response(urls)
            else:
                return Response("Invalid data", status=status.HTTP_403_FORBIDDEN)
        except PyTubeCustomError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
