from django.core.management.base import BaseCommand, CommandError

from catalog.models.movie import Movie


class Command(BaseCommand):
    help = "Show movie info in the Movies Library Metadata Explorer"

    def add_arguments(self, parser):
        parser.add_argument(
            '--all', action='store_true',
            help='List all movies')

        parser.add_argument(
            'movie_ids', nargs='*', type=int,
            help='IDs of movies to show')

    def handle(self, *args, **options):
        if options['all']:
            movies = Movie.objects.all()
        elif options['movie_ids']:
            movies = Movie.objects.filter(id__in=options['movie_ids'])
        else:
            raise CommandError('Must provide a movie id or --all argument')

        for movie in movies:
            output = [f'{movie.title}, {movie.director.last_name}']
            if movie.director.first_name:
                output.append(f', {movie.director.first_name}')
            output.append(f' [id={movie.id}]')
            self.stdout.write(''.join(output))
