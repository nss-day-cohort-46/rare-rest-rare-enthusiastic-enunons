from django.core.exceptions import ValidationError
from django.db.models.fields import DateTimeCheckMixin
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post, Comment, RareUser
from rest_framework.viewsets import ViewSet
from datetime import datetime

class CommentView(ViewSet):
    def create(self, request):
        """Handle POST operations for comments

        Returns:
            Response -- JSON serialized event instance
        """

        author = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["postId"])

        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = datetime.now()
        comment.author = author
        comment.post = post

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests to get all tags
        Returns:
            Response -- JSON serialized list of tags
        """
        comment = Comment.objects.all()
        serializer = CommentSerializer(
            comment, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment

        Returns:
            Response -- JSON serialized comment instance
        """
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single comment

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        """Handle PUT requests for a comment

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        comment = Comment.objects.get(pk=pk)
        author = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk = request.data["postId"])


        comment.content = request.data["content"]
        comment.created_on = datetime.now()
        comment.author = author
        comment.post = post

        try:
            comment.save()
            # 204 status code means everything worked but the
            # server is not sending back any data in the response
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception:
            return HttpResponseServerError(Exception)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_on')