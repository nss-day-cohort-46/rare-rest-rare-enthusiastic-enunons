"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post, RareUser


class PostView(ViewSet):

    def create(self, request):

        rare_user = RareUser.objects.get(user=request.auth.user)

        post = Game()
        game.name = request.data["name"]
        game.difficulty = request.data["difficulty"]
        game.number_of_players = request.data["numberOfPlayers"]

        game_type = GameType.objects.get(pk=request.data["gameTypeId"])
        game.game_type = game_type

        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
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
        fields = ('id', 'user', 'category', 'title', 'publication_date',
                    'image_url', 'content', 'approved')