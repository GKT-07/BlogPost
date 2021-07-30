# from typing_extensions import Required
# from typing_extensions import Required
from django.contrib.auth.models import User
from django.db.models import fields
from django.db.models.base import Model
from .models import BlogModel
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .helpers import *






class BlogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=BlogModel
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8)
    blog = BlogModelSerializer(many=True, required=False)
    votes = BlogModelSerializer(many=True, required=False)
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'blog', 'votes')


