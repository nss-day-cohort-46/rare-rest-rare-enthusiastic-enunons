"""View module for handling requests about posts"""
from django.core.exceptions import ValidationError
from django.db.models.fields import URLField
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post, RareUser, Category
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Q

class PostView(ViewSet):

    def create(self, request):
        
        rare_user = RareUser.objects.get(user=request.auth.user)

        post = Post()
        post.rare_user = rare_user
        post.title = request.data["title"]
        post.publication_date = date.today()
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        category = Category.objects.get(pk=request.data["categoryId"])
        post.category = category

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        rare_user1 = RareUser.objects.get(user=request.auth.user)
        # posts = Post.objects.filter(rare_user=rare_user1)

        # search_terms = self.request.query_params.get('searchTerms', None)
        # if search_terms is not None:
        #     posts = Post.objects.filter(Q(title__contains=search_terms))
        # else:
        #     posts = Post.objects.all()
        
        if request.path=="/myposts":
            posts = Post.objects.filter(rare_user=rare_user1)
        else:
            posts = Post.objects.all()

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, pk=None):

        rare_user = RareUser.objects.get(user=request.auth.user)

        post = Post.objects.get(pk=pk)
        post.rare_user = rare_user
        post.title = request.data["title"]
        post.publication_date = date.today()
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        category = Category.objects.get(pk=request.data["categoryId"])
        post.category = category
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):

        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostUserSerializer(serializers.ModelSerializer):
    """JSON serializer for user's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for rare user"""
    user = PostUserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ['user']

class PostSerializer(serializers.ModelSerializer):

    rare_user = RareUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'rare_user', 'category', 'title', 'publication_date',
                    'image_url', 'content', 'approved')
        