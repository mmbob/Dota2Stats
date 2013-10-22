from django.db import models

# Create your models here.

class Member(models.Model):
	accountID = models.PositiveIntegerField(unique = True, primary_key = True);
	steamID = models.BigIntegerField();
	name = models.CharField(max_length = 100);

class MatchPlayer(models.Model):
	matchID = models.ForeignKey("Match");
	accountID = models.ForeignKey("Member");

	name = models.CharField(max_length = 100);
	level = models.PositiveSmallIntegerField();
	heroID = models.PositiveSmallIntegerField();

	heroDamage = models.PositiveIntegerField();
	towerDamage = models.PositiveIntegerField();
	heroHealing = models.PositiveIntegerField();

	kills = models.PositiveSmallIntegerField();
	deaths = models.PositiveSmallIntegerField();
	assists = models.PositiveSmallIntegerField();

	lastHits = models.PositiveSmallIntegerField();
	denies = models.PositiveSmallIntegerField();
	gold = models.PositiveIntegerField();
	goldPerMinute = models.PositiveSmallIntegerField();
	expPerMinute = models.PositiveSmallIntegerField();

	level6Time = models.PositiveSmallIntegerField();
	level11Time = models.PositiveSmallIntegerField();
	level16Time = models.PositiveSmallIntegerField();

class Match(models.Model):
	id = models.IntegerField(unique = True, primary_key = True);
	startTime = models.PositiveIntegerField();
	duration = models.PositiveIntegerField();
	radiantVictory = models.BooleanField();

	player0 = models.ForeignKey("MatchPlayer");
	player1 = models.ForeignKey("MatchPlayer");
	player2 = models.ForeignKey("MatchPlayer");
	player3 = models.ForeignKey("MatchPlayer");
	player4 = models.ForeignKey("MatchPlayer");
	player5 = models.ForeignKey("MatchPlayer");
	player6 = models.ForeignKey("MatchPlayer");
	player7 = models.ForeignKey("MatchPlayer");
	player8 = models.ForeignKey("MatchPlayer");
	player9 = models.ForeignKey("MatchPlayer");

	radiantBarracksStatus = models.PositiveSmallIntegerField();
	radiantTowerStatus = models.PositiveSmallIntegerField();
	direBarracksStatus = models.PositiveSmallIntegerField();
	direTowerStatus = models.PositiveSmallIntegerField();