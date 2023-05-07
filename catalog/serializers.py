from rest_framework import serializers

from catalog.models.director import Director


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'first_name', 'last_name', 'created', 'updated']
