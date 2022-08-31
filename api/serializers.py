from api.models import Posts
from rest_framework import serializers
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Posts
        exclude=("date",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","first_name","last_name","email","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)