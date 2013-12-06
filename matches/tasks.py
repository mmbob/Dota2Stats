from async import schedule
from Dota2 import webapi
from matches.models import *
import time
from sys import stderr

def parse_player_info(match, player_json):
	account_id = int(player_json.get('account_id', webapi.INVALID_ACCOUNT_ID));
	player_filter = Player.objects.filter(account_id = account_id);

	p = None;

	if player_filter.count() == 0:
		p = Player();
		p.account_id = account_id;
		p.steam_id = webapi.account_to_steam_id(account_id);

		summaries = webapi.get_player_summaries([p.steam_id])['players'];
						
		if len(summaries) != 0:
			p.name = summaries[0]['personaname'];
		else:
			p.name = "Anonymous";
							
		p.save();
	else:
		p = player_filter[0];

	return MatchPlayer.create(match, p, player_json);
					
	mp.save();

def parse_match_info(match_json):
	match_id = int(match_json['match_id']);
	match_filter = Match.objects.filter(id = match_id);
	if match_filter.count() == 0:
		details = webapi.get_match_details(match_id);

		m = Match();
		m.id = match_id;
		m.start_time = details['start_time'];
		m.duration = details['duration'];
		m.radiant_victory = details['radiant_win'];
		m.radiant_barracks_status = details['barracks_status_radiant'];
		m.radiant_tower_status = details['tower_status_radiant'];
		m.dire_barracks_status = details['barracks_status_dire'];
		m.dire_tower_status = details['tower_status_dire'];
		
		teams = [[], []];		# Radiant, Dire

		for player in details['players']:
			mp = parse_player_info(m, player);

			if mp.match_slot < 100:
				teams[0].append(mp);
			else:
				teams[1].append(mp);
		
		for team in teams:
			gold_total = 0;
			for mp in team:
				gold_total += mp.gold_spent + mp.gold;

			for mp in team:
				gold_percent = int(float(mp.gold_spent + mp.gold) / gold_total * 100);
	else:
		m = match_filter[0];

	return m;

def fetch_player_information(account_id):
	last_match_id = 0;

	begin_time = time.clock();
	history = webapi.get_match_history(account_id);
	end_time = time.clock();
	stderr.write('First history time: ' + str(end_time - begin_time));

	next_request_time = 0;

	while history.get('num_results', 0) > 0:

		for match in history['matches']:

			current_time = time.clock();
			if current_time < next_request_time:
				time.sleep(next_request_time - current_time);
				request_time = current_time + 1;

			last_match_id = parse_match_info(match);

		history = webapi.get_match_history(account_id, last_match_id);

		if history.get('results_remaining', 0) == 0:
			break;

	if history['status'] != 1:
		stderr.write('Error while retrieving history: ' + history['statusDetail'] + '\n' + 'Account ID: ' + str(account_id) + '\n');