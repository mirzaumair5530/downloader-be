from rest_framework import serializers


class ResponseSerializer(serializers.Serializer):
    class Meta:
        fields = ["url"]

    url = serializers.CharField(min_length=0, required=True)
