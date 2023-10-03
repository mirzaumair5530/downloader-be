from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from .serializers import ResponseSerializer


class PyTubeCustomError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InstaDownloader(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):

        try:
            url = request.query_params.get("url")
            if not url:
                raise PyTubeCustomError("Please provide Url")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

            # loading the page
            driver.get(url)

            # set maximum time to load the web page in seconds
            driver.implicitly_wait(10)

            videoTag = driver.find_element(By.TAG_NAME, "video")


            if not videoTag:
                return Response(
                    "Something went wrong", status=status.HTTP_400_BAD_REQUEST
                )

            url = videoTag.get_attribute("src")
            data = {"url": url}
            serializer = ResponseSerializer(data=data)

            if serializer.is_valid():
                return Response(data)
            else:
                return Response("Invalid data", status=status.HTTP_403_FORBIDDEN)
        except PyTubeCustomError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
