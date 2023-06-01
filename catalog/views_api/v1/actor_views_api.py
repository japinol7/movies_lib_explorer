from rest_framework import generics
from rest_framework import authentication
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from catalog.models.actor import Actor
from catalog.serializers import ActorSerializer
from catalog.permissions import IsAdminOrReadOnly
from config.config import ERROR_PERMISSION_MSG
from tools.logger.logger import log


class ActorList(generics.ListCreateAPIView):
    """List all actors or create a new actor."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['last_name', 'first_name']
    search_fields = ['last_name', 'first_name']
    ordering_fields = ['last_name', 'first_name']

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            log.info(f"WARNING! Create new actor: {ERROR_PERMISSION_MSG} User: {self.request.user}")
            raise ValidationError(ERROR_PERMISSION_MSG)

        instance = serializer.save()
        log.info(f"Create new actor: {instance!r} User: {self.request.user}")


class ActorDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a actor."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        log.info(f"Update actor: {instance!r} User: {self.request.user}")

    def perform_destroy(self, instance):
        log.info(f"Delete actor: {instance!r} User: {self.request.user}")
        instance.delete()
