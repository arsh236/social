from api.models import Posts
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Posts
        exclude=("date",)
