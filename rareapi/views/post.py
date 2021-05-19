"""View module for handling requests about posts"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post, RareUser, Category

class PostView(ViewSet):

    def create(self, request):
        
        rare_user = RareUser.objects.get(user=request.auth.user)

        post = Post()
        post.rare_user = request.data["user"]
        post.category = request.data["category"]
        post.title = request.data["title"]
        post.publication_date = request.data["publicationDate"]
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
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'rare_user', 'category', 'title', 'publication_date',
                    'image_url', 'content', 'approved')
        depth = 1