from django.core.management.base import BaseCommand

from catalog.models.director import Director


class Command(BaseCommand):
    help = "Lists directors in the Movies Library Metadata Explorer"

    def handle(self, *args, **options):
        for director in Director.objects.all():
            output = [f'{director.last_name}']
            if director.first_name:
                output.append(f', {director.first_name}')
            if director.picture:
                output.append(f' {director.picture.name}')
            else:
                output.append(f' no picture')
            self.stdout.write(''.join(output))
