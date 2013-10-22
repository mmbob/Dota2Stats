import json
import urllib
import string
import django

urls = (
		'/', 'index'
		'/vanity/(.*)', 'vanity'
		'/steamid/\d+', 'steamid'
		);

API_KEY = '81DA969CDBE56A7C87825BC21C9C1339';
INVALID_STEAM_ID = 4294967295 + 76561197960265728;
INVALID_ACCOUNT_ID = 4294967295;

def AccountToSteamID(accountID):
	return int(accountID) + 76561197960265728;

def SteamToAccountID(accountID):
	return int(accountID) - 76561197960265728;

def ResolveVanityURL(urlPart):
	requestURL = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={0}&vanityurl={1}'.format(API_KEY, urlPart);

	response = urllib2.urlopen(requestURL);
	responseString = response.read().decode('utf-8');
	return SteamToAccountID(json.loads(responseString)['response']['steamid']);

def GetMatchHistory(accountID):
	"""Return JSON object containing the match history."""

	requestURL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key={0}&account_id={1}'.format(API_KEY, accountID);
	
	response = urllib2.urlopen(requestURL);
	responseString = response.read().decode('utf-8');
	return json.loads(responseString);

def GetMatchDetails(matchID):
	requestURL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key={0}&match_id={1}'.format(API_KEY, matchID);
	
	response = urllib2.urlopen(requestURL);
	responseString = response.read().decode('utf-8');
	return json.loads(responseString);

def GetPlayerSummaries(steamIDs):
	requestURL = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}'.format(API_KEY, ','.join(steamIDs));
	
	response = urllib2.urlopen(requestURL);
	responseString = response.read().decode('utf-8');
	return json.loads(responseString);

def GetLatestMatchInfo(accountID):
	history = GetMatchHistory(accountID);

	match = history['result']['matches'][0]
	matchInfo = dict();

	matchDetails = GetMatchDetails(match['match_id']);

	steamIDs = [];

	for player in matchDetails['result']['players']:
		matchInfo[player['account_id']] = {'match_result': player, 'name': 'Anonymous'};
		steamIDs.append(str(AccountToSteamID(player['account_id'])));

	summaries = GetPlayerSummaries(steamIDs);

	for summary in summaries['response']['players']:
		accountID = SteamToAccountID(summary['steamid']);
		matchInfo[accountID]['name'] = summary['personaname'];

	return matchInfo;

class index:
	def GET(self):
		return '<a href="vanity/bobitty">here</a>';

class vanity:
	def GET(self, vanityURL):
		matchInfo = GetLatestMatchInfo(ResolveVanityURL(vanityURL));
		for accountID, info in matchInfo.items():
			print(info['name'] + ': ' + str(info['match_result']['hero_damage']));

class steamid:
	def GET(self, steamID):
		matchInfo = GetLatestMatchInfo(SteamToAccountID(steamID));
		for accountID, info in matchInfo.items():
			print(info['name'] + ': ' + str(info['match_result']['hero_damage']));

def main():
	history = GetMatchHistory(ResolveVanityURL('bobitty'));

	for match in history['result']['matches']:
		matchInfo = dict();

		matchDetails = GetMatchDetails(match['match_id']);

		steamIDs = [];

		for player in matchDetails['result']['players']:
			matchInfo[player['account_id']] = {'match_result': player, 'name': 'Anonymous'};
			steamIDs.append(str(AccountToSteamID(player['account_id'])));

		summaries = GetPlayerSummaries(steamIDs);

		for summary in summaries['response']['players']:
			accountID = SteamToAccountID(summary['steamid']);
			matchInfo[accountID]['name'] = summary['personaname'];
		
		for accountID, info in matchInfo.items():
			print(info['name'] + ': ' + str(info['match_result']['hero_damage']));

		input();

		break;

	return 0;

if __name__ == "__main__":
	app = web.application(urls, globals());
	app.run();