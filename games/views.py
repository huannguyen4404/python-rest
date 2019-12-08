from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from games.models import Game
from games.serializers import GameSerializer


# class JSONResponse(HttpResponse):
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content-type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        game_serializer = GameSerializer(games, many=True)
        return JsonResponse(game_serializer.data, safe=False)

    elif request.method == 'POST':
        game_data = JSONParser.parse(request)
        game_serializer = GameSerializer(data=game_data)
        if game_serializer.is_valid():
            game_serializer.save()
            return JsonResponse(game_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def game_detail(request, pk):
    try:
        game = Game.object.get(pk=pk)
    except Game.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        game_serializer = GameSerializer(game)
        return JsonResponse(game_serializer.data)
    elif request.method == 'PUT':
        game_data = JSONParser().parse(request)
        game_serializer = GameSerializer(game, data=game_data)
        if game_serializer.is_valid():
            game_serializer.save()
            return JsonResponse(game_serializer.data)
        return JsonResponse(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        game.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
