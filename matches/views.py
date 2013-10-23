# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

from matches.models import *

def index(request):
	context = {};
	return render(request, 'matches/player.html', context);

def player(request, player_id):
	players = Player.objects.filter(account_id = int(player_id)).values();
	if len(players) == 0:
		return HttpResponse("Player not found");
	elif len(players) == 1:
		context = {'player': players[0]};
		return render(request, 'matches/player.html', context);
	else:
		return HttpResponse("Player not found");

def match(request, match_id):
	matches = Match.objects.filter(id = int(match_id)).values();
	match_players = MatchPlayer.objects.filter(match_id = int(match_id)).values();
	if len(matches) == 0:
		return HTTPResponse("Match not found");
	elif len(matches) == 1:
		context = {'match': matches[0], 'players': match_players};
		return render(request, 'matches/match.html', context);
	else:
		return HttpResponse("Match not found");