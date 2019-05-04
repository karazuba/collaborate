from rest_framework import serializers


class VoteSerializer(serializers.Serializer):
    value = serializers.BooleanField()
