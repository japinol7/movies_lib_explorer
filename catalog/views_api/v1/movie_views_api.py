from rest_framework import generics
from rest_framework import authentication
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django_filters import rest_framework as drf_filters
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from catalog.models.movie import Movie
from catalog.serializers import MovieSerializer
from catalog.permissions import IsAdminOrReadOnly
from catalog.views_api.v1.movie_filters_api import MovieFilter
from config.config import ERROR_PERMISSION_MSG
from tools.logger.logger import log


class MovieList(generics.ListCreateAPIView):
    """List all movies or create a new movie."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,
                       drf_filters.DjangoFilterBackend]
    filterset_class = MovieFilter
    search_fields = ['title', 'title_original', 'director__last_name', 'director__first_name',
                     'year', 'country', 'language', 'cast']
    ordering_fields = ['id', 'title', 'title_original', 'director__last_name', 'director__first_name',
                       'year', 'country', 'language']

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            log.info(f"WARNING! Create new movie: {ERROR_PERMISSION_MSG} User: {self.request.user}")
            raise ValidationError(ERROR_PERMISSION_MSG)

        instance = serializer.save()
        log.info(f"Create new movie: {instance!r} User: {self.request.user}")


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a movie."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        log.info(f"Update movie: {instance!r} User: {self.request.user}")

    def perform_destroy(self, instance):
        log.info(f"Delete movie: {instance!r} User: {self.request.user}")
        instance.delete()
