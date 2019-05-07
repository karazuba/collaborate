from rest_framework import serializers


class BasicVoteSerializer(serializers.Serializer):
    value = serializers.BooleanField()
