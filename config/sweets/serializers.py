from rest_framework import serializers
from .models import Sweet


class SweetSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()

    class Meta:
        model = Sweet
        fields = "__all__"

