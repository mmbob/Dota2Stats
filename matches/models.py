from django.db import models

# Create your models here.

class Player(models.Model):
	account_id = models.PositiveIntegerField(unique = True, primary_key = True);
	steam_id = models.BigIntegerField();
	name = models.CharField(max_length = 100);

	def get_absolute_url():
		return "/players/%d" % self.accountID;

class MatchPlayer(models.Model):
	match = models.OneToOneField("Match");
	account = models.ForeignKey("Player");

	name = models.CharField(max_length = 100);
	level = models.PositiveSmallIntegerField();
	hero_id = models.PositiveSmallIntegerField();

	hero_damage = models.PositiveIntegerField();
	tower_damage = models.PositiveIntegerField();
	hero_healing = models.PositiveIntegerField();

	kills = models.PositiveSmallIntegerField();
	deaths = models.PositiveSmallIntegerField();
	assists = models.PositiveSmallIntegerField();

	last_hits = models.PositiveSmallIntegerField();
	denies = models.PositiveSmallIntegerField();
	gold = models.PositiveIntegerField();
	gold_per_minute = models.PositiveSmallIntegerField();
	exp_per_minute = models.PositiveSmallIntegerField();

	level6_time = models.PositiveSmallIntegerField();
	level11_time = models.PositiveSmallIntegerField();
	level16_time = models.PositiveSmallIntegerField();

class PlayerMatch(models.Model):
	player = models.ForeignKey("Player");
	match = models.ForeignKey("Match");
	match_player = models.ForeignKey("MatchPlayer");

class Match(models.Model):
	id = models.IntegerField(unique = True, primary_key = True);
	start_time = models.PositiveIntegerField();
	duration = models.PositiveIntegerField();
	radiant_victory = models.BooleanField();

	player0 = models.OneToOneField("MatchPlayer", related_name = "player0");
	player1 = models.OneToOneField("MatchPlayer", related_name = "player1");
	player2 = models.OneToOneField("MatchPlayer", related_name = "player2");
	player3 = models.OneToOneField("MatchPlayer", related_name = "player3");
	player4 = models.OneToOneField("MatchPlayer", related_name = "player4");
	player5 = models.OneToOneField("MatchPlayer", related_name = "player5");
	player6 = models.OneToOneField("MatchPlayer", related_name = "player6");
	player7 = models.OneToOneField("MatchPlayer", related_name = "player7");
	player8 = models.OneToOneField("MatchPlayer", related_name = "player8");
	player9 = models.OneToOneField("MatchPlayer", related_name = "player9");

	radiant_barracks_status = models.PositiveSmallIntegerField();
	radiant_tower_status = models.PositiveSmallIntegerField();
	dire_barracks_status = models.PositiveSmallIntegerField();
	dire_tower_status = models.PositiveSmallIntegerField();

	def get_absolute_url():
		return "/matches/%d" % self.id;