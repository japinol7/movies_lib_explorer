from django_filters import rest_framework as filters, IsoDateTimeFilter

from catalog.models.movie import Movie


class MovieFilter(filters.FilterSet):
    created = IsoDateTimeFilter()
    updated = IsoDateTimeFilter()

    class Meta:
        model = Movie
        fields = {
            'title': ['exact'],
            'title_original': ['exact'],
            'director__id': ['exact'],
            'director__last_name': ['exact'],
            'director__first_name': ['exact'],
            'year': ['exact', 'lt', 'gt'],
            'country': ['exact'],
            'language': ['exact'],
            'created': ['exact',
                        'date__gt', 'date__lt', 'date__exact',
                        'time__gt', 'time__lt', 'time__exact',
                        ],
            'updated': ['exact',
                        'date__gt', 'date__lt', 'date__exact',
                        'time__gt', 'time__lt', 'time__exact',
                        ],
        }
