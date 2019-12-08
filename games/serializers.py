from rest_framework import serializers
from games.models import Game

class GameSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    release_date = serializers.DateTimeField()
    game_category = serializers.CharField(max_length=200)
    played = serializers.BooleanField(required=False)

    def create(self, validate_data):
        return Game.objects.create(**validate_data)

    def update(self, instance, validate_data):
        instance.name = validate_data.get('name', instance.name)
        instance.release_date = validate_data.get('release_date', instance.release_date)
        instance.game_category = validate_data.get('game_category', instance.game_category)
        instance.played = validate_data.get('played', instance.played)
        instance.save()
        return instance
