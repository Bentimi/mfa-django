from rest_framework import serializers


class OtpSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=6)