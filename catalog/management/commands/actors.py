from django.core.management.base import BaseCommand

from catalog.models.actor import Actor


class Command(BaseCommand):
    help = "Lists actors in the Movies Library Metadata Explorer"

    def handle(self, *args, **options):
        for actor in Actor.objects.all():
            output = [f'{actor.last_name}']
            if actor.first_name:
                output.append(f', {actor.first_name}')
            if actor.picture:
                output.append(f' {actor.picture.name}')
            else:
                output.append(f' no picture')
            self.stdout.write(''.join(output))
