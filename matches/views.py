# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

from matches.models import *

def index(request):
	context = {};
	return render(request, 'matches/player.html', context);

def player(request, player_id):
	context = {'player_id': player_id, Player.objects.};
	return render(request, 'matches/player.html', context);