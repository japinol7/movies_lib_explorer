from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from catalog.models.director import Director
from catalog.models.movie import Movie


class CommandsTestCase(TestCase):
    def run_command(self, name, *args, **options):
        stdout = StringIO()
        options['stdout'] = stdout
        call_command(name, *args, **options)
        return stdout.getvalue()

    def setUp(self):
        super().setUp()
        self.director = Director.objects.create(first_name='f_name', last_name='l_name')
        self.movie1 = Movie.objects.create(title='title1', director=self.director, year=1900)
        self.movie2 = Movie.objects.create(title='title2', director=self.director, year=1900)

    def test_director(self):
        out = self.run_command('directors')
        self.assertEqual(out.count('\n'), 1)
        self.assertIn('l_name', out)

    def test_movie(self):
        # Test --all
        out = self.run_command('movie', all=True)
        self.assertEqual(out.count('\n'), 2)
        self.assertIn('title1', out)
        self.assertIn('title2', out)

        # Test id argument
        out = self.run_command('movie', self.movie1.id)
        self.assertEqual(out.count('\n'), 1)
        self.assertIn('title1', out)

        # Test error management
        with self.assertRaises(CommandError):
            self.run_command('movie')
