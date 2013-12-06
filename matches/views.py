# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.forms import *

from matches.models import *
from matches.forms import *
from matches.tasks import *
from Dota2 import webapi
from multiprocessing import Process
import openid;

def index(request):
	context = {'players': Player.objects.exclude(account_id = webapi.INVALID_ACCOUNT_ID).values()};
	return render(request, 'matches/index.html', context);

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST);
		if form.is_valid():
			profile_url = str(form.cleaned_data['main']);

#			Match.objects.all().delete();
#			MatchPlayer.objects.all().delete();
#			Player.objects.all().delete();

			p = Player();

			p.account_id = webapi.INVALID_ACCOUNT_ID;

			part_start = profile_url.find('/id/') + 4;
			if part_start == -1 + 4:
				part_start = profile_url.find('/profiles/') + 10;
				if part_start == -1 + 10:
					part_start = 0;

			part_end = len(profile_url);
			if profile_url[-1] == '/':
				part_end -= 1;

			url_part = profile_url[part_start:part_end];

			if profile_url.find('/id/') != -1:
				vanity_info = webapi.resolve_vanity_url(url_part);
				if vanity_info['success'] == 1:
					p.account_id = vanity_info['steamid'];
			if p.account_id == webapi.INVALID_ACCOUNT_ID:
				p.account_id = int(url_part);

			p.account_id = webapi.steam_to_account_id(p.account_id);
			p.steam_id = webapi.account_to_steam_id(p.account_id);

			summaries = webapi.get_player_summaries([p.steam_id]);
			p.name = summaries['players'][0]['personaname'];

			p.save();

			process = Process(target = fetch_player_information, args = (p.account_id, ));
			process.start();

			return HttpResponseRedirect('register/success');
	else:
		form = RegisterForm();

	context = {'form': form};
	return render(request, 'matches/register.html', context);

def player(request, player_id):
	players = Player.objects.filter(account_id = int(player_id)).values();
	if len(players) == 1:
		context = {'player': players[0]};
	else:
		context = {};

	return render(request, 'matches/player.html', context);

def match(request, match_id):
	matches = Match.objects.filter(id = int(match_id)).values();
	match_players = MatchPlayer.objects.filter(match_id = int(match_id)).values();
	if len(matches) == 1:
		context = {'match': matches[0], 'players': match_players};
	else:
		context = {};

	return render(request, 'matches/match.html', context);