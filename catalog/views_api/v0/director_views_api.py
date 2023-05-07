from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalog.models.director import Director
from catalog.serializers import DirectorSerializer


@api_view(['GET', 'POST'])
def director_list(request, format=None):
    """List all directors or create a new director."""
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        content = {
            'directors': serializer.data,
            }
        return Response(content)

    if request.method == 'POST':
        serializer = DirectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail(request, pk, format=None):
    """Retrieve, update or delete a director."""
    try:
        director = Director.objects.get(pk=pk)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DirectorSerializer(director)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = DirectorSerializer(director, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
