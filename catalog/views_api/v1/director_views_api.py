from rest_framework import generics
from rest_framework import authentication
from rest_framework.exceptions import ValidationError

from catalog.models.director import Director
from catalog.serializers import DirectorSerializer
from catalog.permissions import IsAdminOrReadOnly
from config.config import ERROR_PERMISSION_MSG
from tools.logger.logger import log


class DirectorList(generics.ListCreateAPIView):
    """List all directors or create a new director."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            log.info(f"WARNING! Create new director: {ERROR_PERMISSION_MSG} User: {self.request.user}")
            raise ValidationError(ERROR_PERMISSION_MSG)

        instance = serializer.save()
        log.info(f"Create new director: {instance!r} User: {self.request.user}")


class DirectorDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a director."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        log.info(f"Update director: {instance!r} User: {self.request.user}")

    def perform_destroy(self, instance):
        log.info(f"Delete director: {instance!r} User: {self.request.user}")
        instance.delete()
