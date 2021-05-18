"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post


class PostView(ViewSet):

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
        fields = ('id', 'user', 'category', 'title', 'publication_date',
                    'image_url', 'content', 'approved')