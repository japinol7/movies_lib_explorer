from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from catalog.models.director import Director
from catalog.serializers import DirectorSerializer


class DirectorList(generics.ListCreateAPIView):
    """List all directors or create a new director."""
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class DirectorDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a director."""
    permission_classes = [IsAuthenticated]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
