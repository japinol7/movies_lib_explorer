from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalog.models.director import Director
from catalog.serializers import DirectorSerializer


@api_view(["GET"])
def list_directors_api(request):
    directors = Director.objects.all()
    serializer = DirectorSerializer(directors, many=True)
    content = {
        'directors': serializer.data,
        }
    return Response(content)
