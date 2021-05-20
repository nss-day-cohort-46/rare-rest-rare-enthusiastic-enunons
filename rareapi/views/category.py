from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Category
from django.db.models import Q

class CategoryView(ViewSet):

# ****************************************************
# get all
# ****************************************************
    def list(self, request):

        #get search params from request
        #if no search then get all objects
        #else filter

        search_terms = self.request.query_params.get('searchTerms', None)
        if search_terms is not None:
            categories = Category.objects.filter(Q(label__contains=search_terms))
        else:
            categories =  Category.objects.all()

        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


# ****************************************************
# get one
# ****************************************************

    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)


# ****************************************************
# create
# ****************************************************

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized category instance
        """

        category = Category()
        category.label = request.data["label"]

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


# ****************************************************
# update
# ****************************************************

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]
        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


# ****************************************************
# destroy
# ****************************************************

    def destroy(self, request, pk=None):
            """Handle DELETE requests for a single game

            Returns:
                Response -- 200, 404, or 500 status code
            """
            try:
                category = Category.objects.get(pk=pk)
                category.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except Category.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ****************************************************
# serialize
# ****************************************************

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'label')
