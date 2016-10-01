from rest_framework import serializers

class GmailSerializer(serializers.Serializer):
    id = serializers.CharField()
    snippet = serializers.CharField()
