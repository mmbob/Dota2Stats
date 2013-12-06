from urllib import request
import json
import codecs

API_KEY = '81DA969CDBE56A7C87825BC21C9C1339';
INVALID_STEAM_ID = 4294967295 + 76561197960265728;
INVALID_ACCOUNT_ID = 4294967295;

def account_to_steam_id(account_id):
	return int(account_id) + 76561197960265728;

def steam_to_account_id(steam_id):
	return int(steam_id) - 76561197960265728;

def get_json_from_url(url):
	response = request.urlopen(url);
	responseString = response.read().decode('utf-8');

	with codecs.open('json_log.txt', mode = 'a', encoding = 'utf-8') as log_file:
		log_file.write(url);
		log_file.write('\r\n');
		log_file.write(responseString);
		log_file.write('\r\n<<<>>>\r\n');

	return json.loads(responseString);

def resolve_vanity_url(url_part):
	url = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={0}&vanityurl={1}'.format(API_KEY, url_part);

	return get_json_from_url(url)['response'];

def get_match_history(account_id, starting_match_id = None, matches_requested = None):
	"""Return JSON object containing the match history."""

	parameters = "?key=%s&account_id=%d" % (API_KEY, int(account_id));
	if starting_match_id != None:
		parameters += "&start_at_match_id=%d" % int(starting_match_id);
	if matches_requested != None:
		parameters += "&matches_requested=%d" % int(matches_requested);

	url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/' + parameters;
	
	return get_json_from_url(url)['result'];

def get_match_details(match_id):
	url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key={0}&match_id={1}'.format(API_KEY, match_id);
	
	return get_json_from_url(url)['result'];

def get_player_summaries(steam_ids):
	id_list_string = "";
	for id in steam_ids:
		id_list_string += str(id) + ',';
	id_list_string = id_list_string[:-1];

	url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}'.format(API_KEY, id_list_string);
	
	return get_json_from_url(url)['response'];

def get_heroes(language = 'en-us'):
	url = 'https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?key={0}&language={1}'.format(API_KEY, language);

	return get_json_from_url(url)['result'];