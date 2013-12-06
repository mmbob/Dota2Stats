from django.db import models

from Dota2 import webapi

# Create your models here.

class Member(models.Model):
	player = models.ForeignKey("Player");
	
	radiant_win_percent = models.PositiveSmallIntegerField(blank = True, null = True);

class Player(models.Model):
	account_id = models.PositiveIntegerField(unique = True, primary_key = True);
	steam_id = models.BigIntegerField();
	name = models.CharField(max_length = 100);

	def get_absolute_url(self):
		return "/player/%d" % self.account_id;

class Ability(models.Model):
	name = models.CharField(max_length = 100);

class MatchPlayerLevelUp(models.Model):
	match_player = models.ForeignKey("MatchPlayer");

	level = models.PositiveSmallIntegerField();
	time = models.PositiveSmallIntegerField();
	ability_id = models.ForeignKey("Ability");

class MatchPlayer(models.Model):
	UNKNOWN = 'U';
	CARRY = 'C';
	SUPPORT = 'S';
	GANKER = 'G';
	SEMICARRY = 'T';

	ROLE_CHOICES = (
				 (UNKNOWN, 'Unknown'),
				 (CARRY, 'Carry'),
				 (SUPPORT, 'Support'),
				 (GANKER, 'Ganker'),
				 (SEMICARRY, 'Semi-Carry'),
	);


	match = models.ForeignKey("Match");
	match_slot = models.PositiveSmallIntegerField();
	account = models.ForeignKey("Player");

	name = models.CharField(max_length = 100);
	level = models.PositiveSmallIntegerField();
	hero = models.PositiveSmallIntegerField();

	hero_damage = models.PositiveIntegerField();
	tower_damage = models.PositiveIntegerField();
	hero_healing = models.PositiveIntegerField();

	kills = models.PositiveSmallIntegerField();
	deaths = models.PositiveSmallIntegerField();
	assists = models.PositiveSmallIntegerField();

	last_hits = models.PositiveSmallIntegerField();
	denies = models.PositiveSmallIntegerField();
	gold = models.PositiveIntegerField();
	gold_spent = models.PositiveIntegerField();

	gold_per_minute = models.PositiveSmallIntegerField();
	exp_per_minute = models.PositiveSmallIntegerField();

	leaver_status = models.PositiveSmallIntegerField();

	items = models.CommaSeparatedIntegerField(max_length = 4 * 6);		# 3 digit item ID and comma for 6 items
	item0 = models.PositiveSmallIntegerField();
	item1 = models.PositiveSmallIntegerField();
	item2 = models.PositiveSmallIntegerField();
	item3 = models.PositiveSmallIntegerField();
	item4 = models.PositiveSmallIntegerField();
	item5 = models.PositiveSmallIntegerField();

	level6_time = models.PositiveSmallIntegerField(blank = True, null = True);
	level11_time = models.PositiveSmallIntegerField(blank = True, null = True);
	level16_time = models.PositiveSmallIntegerField(blank = True, null = True);

	guessed_role = models.CharField(max_length = 1, choices = ROLE_CHOICES, default = UNKNOWN);

	@staticmethod
	def create(match, player, player_json):
		mp = MatchPlayer();
		mp.match = match;
		mp.match_slot = player_json['player_slot'];
		mp.account = player;
		mp.name = player.name;
		mp.level = player_json['level'];
		mp.hero = player_json['hero_id'];

		mp.leaver_status = player_json.get('leaver_status', 0);

		mp.hero_damage = player_json['hero_damage'];
		mp.tower_damage = player_json['tower_damage'];
		mp.hero_healing = player_json['hero_healing'];

		mp.kills = player_json['kills'];
		mp.deaths = player_json['deaths'];
		mp.assists = player_json['assists'];

		mp.last_hits = player_json['last_hits'];
		mp.denies = player_json['denies'];
		mp.gold = player_json['gold'];
		mp.gold_spent = player_json['gold_spent'];
		mp.gold_per_minute = player_json['gold_per_min'];
		mp.exp_per_minute = player_json['xp_per_min'];

		mp.item0 = player_json.get('item_0', 0);
		mp.item1 = player_json.get('item_1', 0);
		mp.item2 = player_json.get('item_2', 0);
		mp.item3 = player_json.get('item_3', 0);
		mp.item4 = player_json.get('item_4', 0);
		mp.item5 = player_json.get('item_5', 0);

		ability_upgrades = player_json.get('ability_upgrades', []);
		if len(ability_upgrades) > 5:
			mp.level6_time = ability_upgrades[5]['time'];
			if len(ability_upgrades) > 10:
				mp.level11_time = ability_upgrades[10]['time'];
				if len(ability_upgrades) > 15:
					mp.level16_time = ability_upgrades[15]['time'];

		return mp;

class PlayerMatch(models.Model):
	player = models.ForeignKey("Player");
	match = models.ForeignKey("Match");
	match_player = models.ForeignKey("MatchPlayer");

class Match(models.Model):
	id = models.IntegerField(unique = True, primary_key = True);
	start_time = models.PositiveIntegerField();
	duration = models.PositiveIntegerField();
	radiant_victory = models.BooleanField();

	radiant_barracks_status = models.PositiveSmallIntegerField();
	radiant_tower_status = models.PositiveSmallIntegerField();
	dire_barracks_status = models.PositiveSmallIntegerField();
	dire_tower_status = models.PositiveSmallIntegerField();

	def get_absolute_url(self):
		return "/match/%d" % self.id;

class Hero(models.Model):
	id = models.IntegerField(unique = True, primary_key = True);
	name = models.CharField(max_length = 100);

	def update_heroes():
		Hero.objects.all().delete();

		heroes = webapi.get_heroes()['heroes'];

		for hero in heroes:
			h = Hero(id = hero['id'], name = hero['localized_name']);
			h.save();

class Item(models.Model):
	id = models.IntegerField(unique = True, primary_key = True);
	name = models.CharField(max_length = 100);

	def update_items():
		Item.objects.all().delete();

		items = webapi