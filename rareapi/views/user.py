"""View module for handling requests about posts"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import RareUser
from django.contrib.auth.models import User

class RareUserView(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            rare_user = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(rare_user, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        users = RareUser.objects.all()

        serializer = RareUserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):

    """JSON serializer for user's related Django user"""
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_staff', 'username']

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for rare user"""
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ['id', 'bio', 'profile_image_url', 'user']