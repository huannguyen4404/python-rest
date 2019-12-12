from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import FilterSet
from django_filters import (
    NumberFilter,
    DateTimeFilter,
    AllValuesFilter,
)

from games.models import Game, GameCategory, PlayerScore, Player
from games.serializers import (
    GameSerializer, GameCategorySerializer,
    PlayerSerializer, PlayerScoreSerializer, UserSerializer,
)
from games.permissions import IsOwnerOrReadOnly


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response(
            {
                'players': reverse(PlayerList.name, request=request),
                'game-categories': reverse(
                    GameCategoryList.name,
                    request=request,
                ),
                'games': reverse(GameList.name, request=request),
                'scores': reverse(PlayerScoreList.name, request=request),
                'users': reverse(UserList.name, request=request),
            },
        )


class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'game-categories'
    filter_fields = ('name',)
    search_fields = ('^name',)
    ordering = ('name',)
    name = 'gamecategory-list'


class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'game-categories'
    name = 'gamecategory-detail'


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    filter_fields = (
        'name', 'game_category', 'release_date', 'played', 'owner',
    )
    search_fields = ('^name',)
    ordering_fields = ('name', 'release_date',)
    name = 'game-list'

    def perform_create(self, serializer):
        # Pass an additional owner field to the create method
        # To Set the owner to the user received in the request
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    name = 'game-detail'


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_fields = ('name', 'gender',)
    search_fields = ('^name',)
    ordering_fields = ('name',)
    name = 'player-list'


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


class PlayScoreFilter(FilterSet):
    min_score = NumberFilter(field_name='score', lookup_expr='gte')
    max_score = NumberFilter(field_name='score', lookup_expr='lte')
    from_score_date = DateTimeFilter(
        field_name='score_date',
        lookup_expr='gte',
    )
    to_score_date = DateTimeFilter(field_name='score_date', lookup_expr='lte')
    player_name = AllValuesFilter(field_name='player__name')
    game_name = AllValuesFilter(field_name='game__name')

    class Meta:
        model = PlayerScore
        fields = (
            'score',
            'from_score_date',
            'to_score_date',
            'min_score',
            'max_score',
            # player__name will be accessed as player_name
            'player_name',
            # game__name will be accessed as game_name
            'game_name',
        )


class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    filter_class = PlayScoreFilter
    ordering_fields = ('score', 'score_date')
    name = 'playerscore-list'


class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
