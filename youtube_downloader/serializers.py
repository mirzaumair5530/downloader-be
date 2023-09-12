from rest_framework import serializers


class ResponseSerializer(serializers.Serializer):
    class Meta:
        fields = ["quality", "url"]

    quality = serializers.CharField(max_length=10, min_length=0, required=True)
    url = serializers.CharField(min_length=0, required=True)
