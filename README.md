# Super-DuckHunt-Beta

# FINAL REVISION FOR v1.0 BETA
# VERSION 1.1 BETA COMING SOON

Super DuckHunt IRC bot 1.0.5 (Python Version 'PyDuck')
By Neo_Nemesis

HELP PAGE: https://neo-coder-usa.github.io/super-duckhunt-beta/

This would be a sequel, or second installment of the original DuckHunt bot by Menz Agitat.
There are a lot of differences in this new Super DuckHunt, read below to understand how it works,
or visit the HELP PAGE linked above.

-----------------------------------------------------------------------------------------------------
SCRIPT INFO & CONFIGURATION
-----------------------------------------------------------------------------------------------------
Requires: Python v3.12.0

Files: main.py, bot.py, func.py, duckhunt.cnf

TO CONFIGURE:

Open duckhunt.cnf

under section [duckhunt]

server = server address (text)

port = (only 6667)

botname = (def DuckHunt)

botpass = (def '0' optional, leave as '0' if no pass used)

duckchan = (duckhunt #channel)

botmaster = Botmaster1,BotMaster2,Botmaster3,etc.. (botmaster list, no ' , ' for single name

admin = Admin1,Admin2,Admin3 (def '0', optional, leave as '0' is not used)

botmaster requires at least 1 botmaster to exist.

botmaster and admin lists can be changed later thru privmsg commands.

** All other settings can be configured by botmasters thru the bot privmsg commands. **

-----------------------------------------------------------------------------------------------------
USER COMMANDS:
-----------------------------------------------------------------------------------------------------
!bang - shoot a duck when it appears

!bef - befriend a duck when it appears

!reload - reload or unjam gun

!shop - brings up shop menu

!shop [id] - purchases specific player items from the shop

!shop [id] [target] - purchases specific effect items from the shop

!duckstats - view your stats

!duckstats <username> - view specified user's stats

!topduck - view the top 5 duck hunter scores

!lastduck - view when the last duck was seen

!tshot - view all the shots counters

!mshot - view monthly shots counter

!wshot - view weekly shots counter

!dshot - view daily shots counter

!bomb [target] - once you have befriended at least 50 ducks, this command becomes available.

-----------------------------------------------------------------------------------------------------
HOW THE GAME WORKS:
-----------------------------------------------------------------------------------------------------
When a duck spawns in chat: -.,¸¸.-·°'`'°·-.,¸¸.-·°'`'°· \_O<   QUACK

Use !bang to shoot it down

Use !bef to befriend the duck

Every time you use !bang, your gun's reliability is reduced. Once you reach 60% reliability
you will be required to clean your gun. (by using !shop 6)

Every time you use !bang, you use 1 ammo (unless gun is jammed/sabotaged)

When you are out of ammo use !reload (more ammo can be purchased with !shop 2)

-----
TIP:
-----
Keep an eye on your gun stats (viewable with !duckstats). Your gun reliability wears down as you shoot over time. Eventually your
gun may start jamming more often as you use it or get so dirty you can't shoot it anymore. To rememedy this you can purchase gun 
cleaning, with !shop 6 this will restore your gun to its maximum reliability rating. Gun upgrades increase maximum reliability (and also accuracy). You can also purchase Gun Grease with !shop 3, which will make gun reliability last longer for 24 hours. 

-----
TIP:
-----
All confiscated guns are returned after the next duck is shot.

-----
TIP:
-----
You can use !shop 20 to purchase a rain coat, with this new item you are protected from becoming soggy for 24 hours.

-----------------------------------------------------------------------------------------------------
GUN UPGRADES:
-----------------------------------------------------------------------------------------------------
You can upgrade your gun and ammo capacity. Starting stats are 75% accuracy and reliability. Starting ammo is 7 rounds and 3 magazines.

!shop 4 will increase your magazine capacity by 1 round. (Max 12)

!shop 7 will increase accuracy and maximum reliability by 5% (Max 100%)

!shop 13 will increase the totla number of magazines in your stock. (Max 5 magazines)


-----------------------------------------------------------------------------------------------------
STATUS EFFECTS:
-----------------------------------------------------------------------------------------------------
Currently there are two status effects, bedazzlement and soggy. All status effects last for 1 hour.

Bedazzlement - caused by a mirror, (!shop 14) from another player. Makes you miss constantly for 1 hour.

Bedazzlement can be prevented by using Sunglasses (!shop 11)

Soggy - caused by a water bucket or duck bomb (!shop 16, !bomb) from another player. Makes you unable to hunt for 1 hour.

Soggy can be prevented by using Rain Coat (!shop 20)

Soggy can be removed by using Dry Clothes (!shop 12)

-----------------------------------------------------------------------------------------------------
ITEM EFFECTS:
-----------------------------------------------------------------------------------------------------
All item effects last for 24 hours.

Gun Grease - reduces gun wear for 24 hours

Trigger Lock - prevents firing the gun without a duck for 24 hours

Silencer - prevents scaring ducks away for 24 hours

Lucky Charm - earns double xp for 24 hours

Sunglasses - prevents bedazzlement for 24 hours

Accident Insurance - prevents gun confiscation for 24 hours

Rain Coat - prevents soggy for 24 hours

-----------------------------------------------------------------------------------------------------
SHOPPING FOR ITEMS:
-----------------------------------------------------------------------------------------------------
Some item prices and availability will change depending on your stats and effects. Gun purchases get more expensive as you
upgrade your ammo capacity and gun accuracy/reliability. 

SHOP ITEMS:
1 - Single Bullet - adds one bullet to your loaded magazine

	!shop 1
 
2 - Refill Magazine - completely refills 1 magazine

	!shop 2
 
3 - Gun Grease - lubricates gun and makes reliability last longer (for 24 hours)

	!shop 3
 
4 - Magazine Upgrade - increases magazine capacity by 1. You start with 7, you can upgrade up to 12 rounds total.

	!shop 4
 
5 - Return Confiscated Gun - if your gun is confiscated, you can buy it back.

	!shop 5
 
6 - Gun Cleaning - restores lost reliability and lowers chances of gun jamming.

	!shop 6
 
7 - Gun Upgrade - increases overall accuracy and reliability of the gun

	!shop 7
 
8 - Trigger Lock - prevents you from firing the gun when ducks are in the area (for 24 hours)

	!shop 8
 
9 - Silencer - prevents you from scaring away ducks when you shoot (for 24 hours)

	!shop 9
 
10 - Lucky Charm - earn double xp (for 24 hours)

	!shop 10
 
11 - Sunglasses - prevents bedazzlement (for 24 hours)

	!shop 11
 
12 - Dry Clothes - when you are soggy, this will remove the status immediately.

	!shop 12
 
13 - Additional Magazine - add an extra magazine to your equipment.  You start with 3, max is 5.

	!shop 13
 
14 - Mirror - cause bedazzlement to a target (for 1 hour)

	!shop 14 TargetUserName
 
15 - Handful of Sand - reduce targets gun reliability by 20%

	!shop 15 TargetUserName
 
16 - Water Bucket - make the target soggy (unable to hunt for 1 hour)

	!shop 16 TargetUserName
 
17 - Sabotage - sabotage target's gun (for 1 turn)

	!shop 17 TargetUserName
 
18 - Accident Insurance - prevents gun confiscation (for 24 hours)

	!shop 18
 
19 - Bread - 'Ammo' for befriending ducks

	!shop 19
 
20 - Rain_Coat - Prevents being soggy (for 24 hours)

	!shop 20

-----------------------------------------------------------------------------------------------------
BOTMASTER AND ADMIN CONTROLS:
-----------------------------------------------------------------------------------------------------

!spawnduck - spawns a random duck (botmaster and admin)

!spawnduck normal - spawns a normal duck (botmaster only)

!spawnduck golden - spawns a duck with ability to turn golden (botmaster only)

!rearm - rearms you (botmaster and admin)

!rearm username - rearms specified user name (botmaster and admin)

!rearm all - rearms all players who have confiscated guns (botmater and admin)

!exit - shuts down the bot (botmaster only)

!flood - flood protection over ride, if flood control is activated it can be automatically deactivated with !flood (botmaster only)

-----------------------------------------------------------------------------------------------------
/msg BotName spawnduck <normal/golden>
-----------------------------------------------------------------------------------------------------

	/msg BotName spawnduck --> Spawns a random duck (botmaster and admin)
	
	/msg BotName spawnduck normal --> Spawns a normal duck (no golden ability) (botmaster only)

	/msg BotName spawnduck golden --> Spawns a duck with ability to turn golden (botmaster only)

-----------------------------------------------------------------------------------------------------
/msg BotName set <maxducks/spawntime/flytime/duckexp/duckfear/duckgold/friendrate/gunricochet/flood> <value> <ext value>
(BOTMASTER ONLY)
-----------------------------------------------------------------------------------------------------

	maxducks = Maximum amount of ducks that can be spawned at once (recommend 3)
 
	/msg BotName set maxducks 3

	spawntime = Time in seconds for spawning a duck (recommend 600 seconds = 10 min)
 
	/msg BotName set spawntime 600

	flytime = Time in seconds until duck flys away (recommend 450 seconds = 7.5 min)
 
	/msg BotName set flytime 450

	duckexp = Amount of xp earned for shooting a regular duck. (Golden ducks are 3x duckexp) (recommend 15xp)
 
	/msg BotName set duckexp 15

	duckfear = Amount of total fear points needed for duck to get scared (recommend 45)
 
	/msg BotName set duckfear 45

	duckgold = Percentage of ducks randomly spawned that can potentially turn golden (recommend 40%)
 
	/msg BotName set duckgold 40

	friendrate = Percentage of success when using !bef (recommend 50%)
 
	/msg BotName set friendrate 50

	gunricochet = Percentage of missed shots that could ricochet (recommend 10%)
 
	/msg BotName set gunricochet 10

	flood = Controls flood protection.
 
	/msg BotName set flood off --> Turns off flood protection
 
	/msg BotName set flood --> Returns the current flood protection status
 
	/msg BotName set flood on X,Y --> Sets the flood setting
 
		X,Y = X = number of commands (recommend 24)
  
		X,Y = Y = number of seconds (recommend 25)
  
	/msg BotName set flood on 24,25 --> sets flood protection to 24 requests in 25 seconds

-----------------------------------------------------------------------------------------------------
/msg BotName add <admin/ignore/botmaster> <username>

(BOTMASTER has full control, ADMIN can only add ignore)	
-----------------------------------------------------------------------------------------------------

	admin = admin list (botmasters only)
 
	/msg BotName add admin Username --> Adds username to the admin list
	
	ignore = ignore list (botmasters and admin)
 
	/msg BotName add ignore Username --> Adds username to the ignore list

	botmaster = botmaster list (botmasters only)
 
	/msg BotName add botmaster Username --> Adds username to the botmaster list

-----------------------------------------------------------------------------------------------------
/msg BotName del <admin/ignore/botmaster> <username>

(BOTMASTER has full control, ADMIN can only add ignore)	
-----------------------------------------------------------------------------------------------------

	admin = admin list (botmasters only)
 
	/msg BotName del admin Username --> removes username from the admin list
	
	ignore = ignore list (botmasters and admin)
 
	/msg BotName del ignore Username --> removes username from the ignore list

	botmaster = botmaster list (botmasters only) (if only 1 botmaster it will not remove)
 
	/msg BotName del botmaster Username --> removes username from the botmaster list
