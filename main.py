#! /usr/bin/python3
# ABOUT INFO# ==========================================================================================================
# Title..........: Super DuckHunt v1.0 Python IRC Bot (BETA)
# File...........: main.py
# Python version.: v3.12.0 (does not work in older versions)
# Script version.: v1.0.5 BETA
# Remarks........: This is the most current version 1.0.5 the final v1.0 release
#                : All bugs found please report, some bugs are already known.
#                : Final change before beginning version 1.1
# Language.......: English
# Description....: IRC Bot Script based off original DuckHunt bot by Menz Agitat
#                  Lots of changes and twists added to this, following suit as Menz Agitat bot was said to be a "port"
#                  of the NES game for IRC, This one would be equivelent to a SNES version, or a "sequel".
# Imports........: func.py, bot.py, configparser, threading, socket, time, random, math
# Author(s)......: Neo_Nemesis (aka coderusa, Neo`Nemesis)
# Modified.......:
# Contributors...: bildramer, Friithian, ComputerTech, esjay, TheFatherMind, [Neo from Freenode], End3r
# ======================================================================================================================

# BETA NOTES # =========================================================================================================
# THANKS TO: bildramer, Friithian, ComputerTech, End3r, TheFatherMind, foxy, Mrinfinity, wez, esjay, vurtual_
# \x02bold test\x02
# \x034color test\x03
# PRIVMSG #TestWookie :\x01ACTION action test\x01
# .../|\ ^._.^ /|\... custom version(s) ??? ;)
# 14,1-.,¸¸.-·°'`'°·-.,¸¸.-·°'`'°·0,1 /|\ ^4.0_4.0^ /|\
# TO DO LIST POSSIBILITIES - UPCOMING VERSION 1.1+ UPDATE GOODIES # ====================================================
# Add the laughing dog (optional feature, can be turned on/off)
# Recode !bang
# Usernames with brackets {} [] seem to cause !shop errors
# Make Golden Ducks more spawnable
# Make Lucky Charm give random 5 - 10 xp instead of double
# Add searching the bushes
# Tweak reliability and gun jamming
# Expand and fix !bomb
# Expand !shop
# Expand/add new timed items/effects
# Add !swim and !shower?? (for !bomb)
# Add an accidental goose?
# Expand botmaster/admin controls
# New shop items, explosive ammo, eye drops
# IMPORT # =============================================================================================================
from configparser import RawConfigParser
from datetime import date
# import datetime
import threading
import socket
import time
import random
import math
import func
import bot

# CONFIGURATION VARIABLES # ============================================================================================
# Do not change these variables here. Instead change them in duckhunt.cnf under section [duckhunt]
# You MUST first manually put the info into duckhunt.cnf under section [duckhunt] before running the bot
# ======================================================================================================================
server = func.cnfread('duckhunt.cnf', 'duckhunt', 'server').lower()
port = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'port'))
duckchan = func.cnfread('duckhunt.cnf', 'duckhunt', 'duckchan').encode()
botname = func.cnfread('duckhunt.cnf', 'duckhunt', 'botname').encode()
botpass = str(func.cnfread('duckhunt.cnf', 'duckhunt', 'botpass'))
botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster')
adminlist = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin')
botignore = func.cnfread('duckhunt.cnf', 'duckhunt', 'ignore')
spawntime = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'spawntime'))
flytime = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'flytime'))
maxducks = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'maxducks'))
duckexp = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'duckexp'))
duckfear = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'duckfear'))
gunricochet = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'gunricochet'))
duckgold = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'duckgold'))
friendrate = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'friendrate'))
# FLOOD CHECK VALUE # ==================================================================================================
flood_check = False
if func.cnfread('duckhunt.cnf', 'duckhunt', 'floodcheck') != '0':
    flood_check = True
# GLOBAL VARIABLES # ===================================================================================================
botversion = b'1.0.5'  # Current Bot Version hard code DO NOT CHANGE
userlist = {}  # For channel user monitoring
userchan = 0  # For channel user monitoring
duckexists = False  # does a duck exist? always leave this as false
# =========================================================
duckhunt = True  # Main duckhunt control
# =========================================================
isconnect = False  # Determines if server is connected, always leave this false
exitvar = False  # For duck_timer, always leave this False
jammedguns = ''  # jammed gun user storage, stored by user name
confiscatedguns = ''  # confiscated gun user storage, stored by user name
fear_factor = False  # for accumulation of duckfear points, always leave this false
flood = 0  # For flood control
flood_time = time.time()  # For flood control
flood_cont = False  # For flood control
flood_timer = ''  # For flood control
duck = {}  # Duck spawn array
duckid = ''  # duck id for !bang/!bef
start_time = ''  # start_time for duck timer
elapsed_time = ''  # for duck timer
daily = func.cnfread('duckhunt.cnf', 'top_shot', 'daily')  # daily shots
weekly = func.cnfread('duckhunt.cnf', 'top_shot', 'weekly')  # weekly shots
monthly = func.cnfread('duckhunt.cnf', 'top_shot', 'monthly')  # monthly shots
totalshot = func.cnfread('duckhunt.cnf', 'top_shot', 'totalshot')  # total shots
month = func.cnfread('duckhunt.cnf', 'top_shot', 't_month')
week = func.cnfread('duckhunt.cnf', 'top_shot', 't_week')
day = func.cnfread('duckhunt.cnf', 'top_shot', 't_day')


# FUNCTIONS ============================================================================================================

# BLANK FUNCTION BOX (TEMPORARY BETA ONLY)
# FUNCTION #============================================================================================================
# Name...........:
# Description....:
# Syntax.........:
# Parameters.....:
# Return values..:
# Author.........:
# Modified.......:
# ======================================================================================================================

# CORE FUNCTIONS LIST # ================================================================================================
# These are functions that require using socket irc.send() or data maps - SEE bot.py and func.py for other functions!
# ======================================================================================================================
# duck_exists
# ducksave
# duckstats
# duck_timer
# fleeduck
# ircnamesrf
# level_up
# namecheck
# shopmenu
# spawnduck
# topduck
# top_shot
# ======================================================================================================================

# FUNCTION #============================================================================================================
# Name...........: duck_exists
# Description....: determines if any spawned ducks exist
# Syntax.........: duck_exists()
# Parameters.....: None
# Return values..: Returns True - Duck Exists
#                  Returns False - Duck Does Not Exist
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def duck_exists():
    for zx in range(maxducks + 1):
        if zx == 0:
            continue
        dkey = 'd' + str(zx)
        if duck[dkey] == 'None':
            continue
        elif duck[dkey] != 'None':
            return True
    return False


# ===> duck_exists

# FUNCTION #============================================================================================================
# Name...........: duckstats
# Description....: Retreives and delivers statistics of requested player
# Syntax.........: duckstats(user, ruser)
# Parameters.....: user - username to send data to
#                  ruser - username of stats to be displayed
# Return values..: Returns 1 after sending stats to user.
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
# noinspection PyUnboundLocalVariable,PySimplifyBooleanCheck,PyShadowingNames
def duckstats(user, ruser):
    # No stats/user hasn't played
    if func.cnfexists('duckhunt.cnf', 'ducks', str(ruser)) is False and isconnect is True:
        irc.send(b'PRIVMSG ' + duckchan + b' :' + ruser + b' > Has not played yet.\r\n')
        return 1
    # prep stats
    bot.iecheck(str(ruser))
    rounds = func.gettok(bot.duckinfo(ruser, b'ammo'), 0, '?').encode()
    mags = func.gettok(bot.duckinfo(ruser, b'ammo'), 1, '?').encode()
    mrounds = func.gettok(bot.duckinfo(ruser, b'ammo'), 2, '?').encode()
    mmags = func.gettok(bot.duckinfo(ruser, b'ammo'), 3, '?').encode()
    ducks = bot.duckinfo(ruser, b'ducks').encode()
    gducks = bot.duckinfo(ruser, b'gducks').encode()
    xp = bot.duckinfo(ruser, b'xp').encode()
    level = bot.duckinfo(ruser, b'level').encode()

    accuracy = func.gettok(bot.duckinfo(ruser, b'guninfo'), 0, '?').encode()
    reliability = func.gettok(bot.duckinfo(ruser, b'guninfo'), 1, '?').encode()
    mreliability = func.gettok(bot.duckinfo(ruser, b'guninfo'), 2, '?').encode()
    if float(reliability) <= 50:
        gunstatus = b'Needs cleaning'
    elif func.istok(jammedguns, str(username), ',') is True:
        gunstatus = b'Jammed'
    elif func.istok(confiscatedguns, str(username), ',') is True:
        gunstatus = b'Confiscated'
    else:
        gunstatus = b'OK'
    if bot.duckinfo(ruser, b'best') == 0:
        besttime = b'NA'
    if bot.duckinfo(ruser, b'best') != 0:
        besttime = bot.duckinfo(ruser, b'best').encode()
    accidents = bot.duckinfo(ruser, b'accidents').encode()
    bread = func.gettok(bot.duckinfo(ruser, b'bread'), 0, '?').encode()
    mbread = func.gettok(bot.duckinfo(ruser, b'bread'), 1, '?').encode()
    friend = bot.duckinfo(ruser, b'friend').encode()

    scorebox = b'[SCORE] Best Time: ' + besttime + b' | Level: ' + level + b' | xp: ' + xp + b' | Ducks: ' + ducks + b' | Golden Ducks: ' + gducks + b' | Befriended Ducks: ' + friend + b' | Accidents: ' + accidents + b' [BREAD BOX] ' + bread + b'/' + mbread
    gunbox = b'[GUN STATS] Status ' + gunstatus + b' | Rounds: ' + rounds + b'/' + mrounds + b' | Magazines: ' + mags + b'/' + mmags + b' | Accuracy: ' + accuracy + b'% | Current Reliability ' + reliability + b'% | Max Reliability: ' + mreliability + b'%'
    hbe = bot.inveffect(str(ruser))
    if isconnect is True:
        irc.send(b'NOTICE ' + user + b' :[Super DuckHunt Stats: ' + ruser + b'] ' + scorebox + b' ' + gunbox + b'\r\n')
        irc.send(b'NOTICE ' + user + b' :[Super DuckHunt Stats: ' + ruser + b'] ' + bytes(str(hbe), 'utf-8') + b'\r\n')
    return 1


# ===> duckstats

# FUNCTION #============================================================================================================
# Name...........: duck_timer
# Description....: Handles duck spawn and escape.
# Syntax.........: duck_timer()
# Parameters.....: None
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
# Continuous Timer Function base - Provided by ComputerTech
# def continuous_timer():
#   start_time = time.time()
#   while True:
#      time.sleep(1)  # Wait for 1 second
#      elapsed_time = time.time() - start_time
#      print(f"Timer: {elapsed_time} seconds")

# main loop stuff
# timer_thread = threading.Thread(target=continuous_timer)
# timer_thread.start()

# noinspection PyUnboundLocalVariable
def duck_timer():
    global exitvar
    if not exitvar:

        # global declarations
        global duckexists
        duckexists = False
        global fear_factor
        fear_factor = False
        global start_time
        start_time = time.time()
        global elapsed_time
        global duck
        duck = {}
        # assigns duck variables based off maxducks (duck timers)
        for dks in range(maxducks + 1):
            if dks == 0:
                continue
            dkey = 'd' + str(dks)
            dval = 'None'
            duck[dkey] = dval
            # print(dkey + ': ' + duck[dkey])
            continue
    if exitvar == 'Connect':
        exitvar = False
    # timer loop
    while True:
        # this kills the timer on script exit or disconnect ====================================================================
        if exitvar is True or exitvar == 'Disconnect':
            break

        # duck spawn/flee timer handling =======================================================================================
        if not duckhunt:
            continue
        time.sleep(10)  # fastest this way ¯\_(o.O)_/¯
        elapsed_time = time.time() - start_time
        # checks for duck openings and spawn/flee timers
        for jx in range(maxducks + 1):
            if jx == 0:
                continue
            # spawn a duck
            if round(elapsed_time) >= spawntime:
                dkey = 'd' + str(jx)
                if duck[dkey] == 'None':
                    # determines if gold or normal duck is spawned based of duckgold value
                    roldgold = random.randrange(0, 100, 1)
                    # duck has ability to turn golden
                    if roldgold <= duckgold:
                        spawnduck(dkey, 'gold')
                        start_time = time.time()
                        break
                    # normal duck
                    if roldgold > duckgold:
                        spawnduck(dkey, 'normal')
                        start_time = time.time()
                        break
            # duck flies away
            if round(elapsed_time) >= flytime:
                dkey = 'd' + str(jx)
                if duck[dkey] != 'None':
                    elapsed_time = float(time.time()) - float(func.gettok(duck[dkey], 0, ','))
                    if round(elapsed_time) >= flytime:
                        fleeduck(dkey)
                        start_time = time.time()
                        break
            continue


# ===> duck_timer

# FUNCTION #============================================================================================================
# Name...........: fleeduck
# Description....: The duck has flown away.
# Syntax.........: fleedduck(d_id)
# Parameters.....: d_id = the duck ID. d1, d2 etc.
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def fleeduck(d_id):
    global fear_factor
    duck[d_id] = 'None'
    if not duck_exists():
        fear_factor = False
    if isconnect:
        irc.send(
            b"PRIVMSG " + duckchan + b" :The duck flies away.     \x0314\xc2\xb7\xc2\xb0'`'\xc2\xb0-.,\xc2\xb8\xc2\xb8.\xc2\xb7\xc2\xb0'`\r\n")
    # start_time = time.time()
    return


# ===> fleeduck

# FUNCTION #============================================================================================================
# Name...........: ircnamesrf
# Description....: This handles the user list and parsing /NAMES command
# Syntax.........: ircnamesrf(namesdata, ext)
# Parameters.....: namesdata - the data string from /NAMES numeric 353
#                  ext - optional (see example below)
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# Example........: ircnamesrf('String Containung User Names') - parses the list into the userlist
#                  ircnamesrf('0', 'r') - resets the userlist to be refreshed with new data
# ======================================================================================================================
def ircnamesrf(namesdata, ext=''):
    global userlist
    global userchan
    names = ''
    if ext == 'r':
        userlist = {}
        userchan = 0
        return
    userchan += 1
    if func.numtok(namesdata, ':') == 3:
        names = func.gettok(namesdata, 2, ':')
    if func.numtok(namesdata, ':') < 3:
        names = func.gettok(namesdata, 1, ':')
    names = names.replace('@', '')
    names = names.replace('&', '')
    names = names.replace('~', '')
    names = names.replace('!', '')
    names = names.replace('%', '')
    names = names.replace('+', '')
    names = names.replace("b'", '')
    names = names.replace("'", '')
    # names = names.replace(']', '')
    names = names.replace(',', '')
    nd_key = 'cl' + str(userchan)
    userlist[nd_key] = names
    # print(' * NAMES ' + str(nd_key) + ': ' + names)
    return


# ===> ircnamesrf

# FUNCTION #============================================================================================================
# Name...........: level_up
# Description....: Level's up specified player
# Syntax.........: level_up(user)
# Parameters.....: user - username to be leveled up
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
# noinspection PyShadowingNames
def level_up(user):
    # fill ammo
    ammo = bot.duckinfo(user, b'ammo')
    mrounds = func.gettok(ammo, 2, '?')
    rounds = mrounds
    mmags = func.gettok(ammo, 3, '?')
    mags = mmags
    ammo = rounds + '?' + mags + '?' + mrounds + '?' + mmags
    bot.duckinfo(user, b'ammo', str(ammo))

    # fill bread
    breadbox = bot.duckinfo(user, b'bread')
    mbread = func.gettok(breadbox, 1, '?')
    bread = mbread
    breadbox = bread + '?' + mbread
    bot.duckinfo(user, b'bread', str(breadbox))

    # increase level by 1
    level = bot.duckinfo(user, b'level')
    level = int(level) + 1
    bot.duckinfo(user, b'level', str(level))

    # increase level up
    xp = bot.duckinfo(user, b'xp')
    levelup = int(xp) + 400
    bot.duckinfo(user, b'levelup', str(levelup))

    # draw prizes
    drawprize = random.randrange(1, 4, 1)
    prize = ''
    prizedesc = ''
    # prize 1 - accident insurance
    if int(drawprize) == 1:
        prize = 'Accident Insurance'
        prizedesc = 'This will prevent gun confiscation for 24 hours.'
        func.cnfwrite('duckhunt.cnf', 'accident_insurance', str(user), str(time.time()))
    # prize 2 - lucky charm
    if int(drawprize) == 2:
        prize = 'Lucky Charm'
        prizedesc = 'You will earn double xp for 24 hours.'
        func.cnfwrite('duckhunt.cnf', 'lucky_charm', str(user), str(time.time()))
    # prize 3 - silencer
    if int(drawprize) == 3:
        prize = 'Silencer'
        prizedesc = 'Your gun will not scare away ducks for 24 hours.'
        func.cnfwrite('duckhunt.cnf', 'accident_insurance', str(user), str(time.time()))
    # prize 4 - sunglasses
    if int(drawprize) == 4:
        prize = 'Sunglasses'
        prizedesc = 'You are protected from bedazzlement for 24 hours.'
        func.cnfwrite('duckhunt.cnf', 'accident_insurance', str(user), str(time.time()))
    # level up confirmation
    if isconnect:
        irc.send(b'NOTICE ' + user + b' :[LEVEL UP] Level: ' + bytes(str(level),
                                                                     'utf-8') + b' [PRIZES] Ammo and bread refilled! You won a ' + bytes(
            str(prize), 'utf-8') + b'! ' + bytes(str(prizedesc), 'utf-8') + b' [AMMO - Rounds: ' + bytes(str(rounds),
                                                                                                         'utf-8') + b'/' + bytes(
            str(mrounds), 'utf-8') + b' | Magazines: ' + bytes(str(mags), 'utf-8') + b'/' + bytes(str(mmags),
                                                                                                  'utf-8') + b'] [BREAD BOX: ' + bytes(
            str(bread), 'utf-8') + b'/' + bytes(str(mbread), 'utf-8') + b']\r\n')
    return


# ===> level_up

# FUNCTION #============================================================================================================
# Name...........: namecheck
# Description....: checks the userlist for a username
# Syntax.........: namecheck(username)
# Parameters.....: username - the named to be searched for in user list
# Return values..: Returns True - user exists in user list (on channel)
#                  Returns False - user does not exist in user list (not on channel)
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def namecheck(name):
    namech = name.replace("b'", '')
    namech = namech.replace("'", '')
    # print('userchan ' + str(userchan))
    nnx = 1
    while nnx <= userchan:
        nd_key = 'cl' + str(nnx)
        print('NAMES: ' + str(userlist[nd_key]))
        if func.istok(userlist[nd_key], namech, ' '):
            return True
        if func.istok(userlist[nd_key], namech + ']', ' '):
            return True

        #if not func.istok(userlist[nd_key], namech, ' ') or not func.istok(userlist[nd_key], str(namech) + ']', ' '):
        #    nnx += 1
        #    continue
        # if func.istok(userlist[nd_key], namech, ' '):
        #    return True
        # bug fix for user name issues
        # namech = namech.replace(']', '')
        # if func.istok(userlist[nd_key], namech + ']', ' '):
        #    return True
        nnx += 1
        continue
    return False


# ===> namecheck

# FUNCTION #============================================================================================================
# Name...........: shopmenu
# Description....: Builds and sends the shop menu to user
# Syntax.........: shopmenu(user)
# Parameters.....: user - requesting username
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def shopmenu(user):
    # ammo = bot.duckinfo(user, b'ammo')
    # rounds = func.gettok(ammo, 0, '?')
    # mags = func.gettok(ammo, 1, '?')
    # mrounds = func.gettok(ammo, 2, '?')
    # mmags = func.gettok(ammo, 3, '?')

    # single bullet
    shop1 = '1: Single Bullet (' + str(bot.shopprice(user, 1)) + ' xp)'
    # refill magazine
    shop2 = '2: Refill Magazine (' + str(bot.shopprice(user, 2)) + ' xp)'
    # gun grease
    shop3 = '3: Gun Grease (' + str(bot.shopprice(user, 3)) + ' xp)'
    # magazine upgrade
    shop4 = '4: Magazine Upgrade (' + str(bot.shopprice(user, 4)) + ' xp)'
    # return confiscated gun
    shop5 = '5: Return Confiscated Gun (' + str(bot.shopprice(user, 5)) + ' xp)'
    # gun cleaning
    shop6 = '6: Gun Cleaning (' + str(bot.shopprice(user, 6)) + ' xp)'
    # gun upgrade
    shop7 = '7: Gun Upgrade (' + str(bot.shopprice(user, 7)) + ' xp)'
    # Gun Lock
    shop8 = '8: Gun Lock (' + str(bot.shopprice(user, 8)) + ' xp)'
    # silencer
    shop9 = '9: Silencer (' + str(bot.shopprice(user, 9)) + ' xp)'
    # lucky charm
    shop10 = '10: Lucky Charm (' + str(bot.shopprice(user, 10)) + ' xp)'
    # sunglasses
    shop11 = '11: Sunglasses (' + str(bot.shopprice(user, 11)) + ' xp)'
    # dry clothes
    shop12 = '12: Dry Clothes (' + str(bot.shopprice(user, 12)) + ' xp)'
    # additional magazine
    shop13 = '13: Additional Magazine (' + str(bot.shopprice(user, 13)) + ' xp)'
    # mirror
    shop14 = '14: Mirror (' + str(bot.shopprice(user, 14)) + ' xp)'
    # handful of sand
    shop15 = '15: Handful of Sand (' + str(bot.shopprice(user, 15)) + ' xp)'
    # water bucket
    shop16 = '16: Water Bucket (' + str(bot.shopprice(user, 16)) + ' xp)'
    # sabotage
    shop17 = '17: Sabotage (' + str(bot.shopprice(user, 17)) + ' xp)'
    # accident insurance
    shop18 = '18: Accident Insurance (' + str(bot.shopprice(user, 18)) + ' xp)'
    # loaf of bread
    shop19 = '19: Loaf of Bread (' + str(bot.shopprice(user, 19)) + ' xp)'
    # rain coat
    shop20 = '20: Rain Coat (' + str(bot.shopprice(user, 20)) + ' xp)'

    # prepares menu
    menu1 = '[Super DuckHunt Shop Menu] ' + shop1 + ' | ' + shop2 + ' | ' + shop3 + ' | ' + shop4 + ' | ' + shop5 + ' | ' + shop6 + ' | ' + shop7 + ' | ' + shop8 + ' | ' + shop9 + ' | ' + shop10
    menu2 = '[Super DuckHunt Shop Menu] ' + shop11 + ' | ' + shop12 + ' | ' + shop13 + ' | ' + shop14 + ' | ' + shop15 + ' | ' + shop16 + ' | ' + shop17 + ' | ' + shop18 + ' | ' + shop19 + ' | ' + shop20
    if isconnect:
        irc.send(b'NOTICE ' + user + b' :' + bytes(str(menu1), 'utf-8') + b'\r\n')
        irc.send(b'NOTICE ' + user + b' :' + bytes(str(menu2), 'utf-8') + b'\r\n')
        irc.send(b'NOTICE ' + user + b' :Syntax: !shop [id] [target]\r\n')
    return


# ===> shopmenu

# FUNCTION #============================================================================================================
# Name...........: spawnduck
# Description....: spawns a duck into chat, if maxducks is not reached
# Syntax.........: spawnduck(d_id, type)
# Parameters.....: d_id = the duck ID. d1, d2 etc
#                  type = normal or gold
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def spawnduck(d_id, d_type):
    global fear_factor
    if duck[d_id] == 'None':
        duck_dat = str(time.time()) + ',' + d_type
        duck[d_id] = str(duck_dat)
        if fear_factor is False:
            fear_factor = 0
        if isconnect:
            irc.send(
                b'PRIVMSG ' + duckchan + b" :\x0314-.,\xc2\xb8\xc2\xb8.-\xc2\xb7\xc2\xb0'`'\xc2\xb0\xc2\xb7-.,\xc2\xb8\xc2\xb8.-\xc2\xb7\xc2\xb0'`'\xc2\xb0\xc2\xb7\x0f \x02\\_O<\x02   \x0314QUACK\x0f\r\n")
        # start_time = time.time()
        return


# ===> spawnduck

# FUNCTION #============================================================================================================
# Name...........: topduck
# Description....: Displays the current top 5 players (could use refining, but works)
# Syntax.........: topduck()
# Parameters.....: None
# Return values..: None - displays topduck message in duckchan
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================

def topduck():
    # No players?
    if func.cnfread('duckhunt.cnf', 'ducks', 'cache') == '0':
        # if isconnect:
        irc.send(b'PRIVMSG ' + duckchan + b' :There are currently no top ducks.\r\n')
        return 1
    # if func.cnfexists('duckhunt.cnf', 'ducks', 'cache') == False:
    #     func.cnfwrite('duckhunt.cnf', 'ducks', 'cache', '0')
    # Gather score information
    parser = RawConfigParser()
    parser.read('duckhunt.cnf')
    datt = ''
    for name, value in parser.items('ducks'):
        datkey = '%s' % name
        if datkey == 'cache':
            continue
        print(datkey)
        dat = func.cnfread('duckhunt.cnf', 'ducks', datkey)
        print(dat)
        xp = func.gettok(dat, 3, ',') + '?' + str(datkey)
        exp = func.gettok(dat, 3, ',')
        if int(exp) == 0:
            continue
        if datt != '':
            datt = datt + ',' + xp
            continue
        if datt == '':
            datt = str(xp)
            continue
    print('GATHER: ' + str(datt))

    # Determine if only 1 top duck or multiple, if more than one, continues if not, sends message.
    if func.numtok(datt, ',') == 1:
        print('only one top duck')
        usr = func.gettok(datt, 0, ',')
        print('USER: ' + str(usr))
        if isconnect:
            irc.send(b'PRIVMSG ' + duckchan + b' :The top duck is: ' + func.gettok(usr, 1,
                                                                                   "'").encode() + b' ' + func.gettok(
                datt, 0, '?').encode() + b' xp\r\n')
        return 1

    # Determine the top 5 scores and assemble into a token string
    vx = 0
    topducklist = ''
    ntok = func.numtok(datt, ',') - 1
    while vx <= ntok:
        rdat = func.gettok(datt, vx, ',')
        if topducklist != '':
            td = func.gettok(rdat, 0, '?')
            topducklist.append(int(td))
            vx += 1
            continue
        if topducklist == '':
            td = func.gettok(rdat, 0, '?')
            topducklist = [int(td)]
            vx += 1
            continue

    # sort the top 5 scores in order
    topducklist.sort(reverse=True)

    # attach usernames to appropriate scores and assemble into token string
    ds = 0
    sc = 0
    totaltop = func.numtok(datt, ',')
    topducks = ''
    while ds <= ntok:
        if func.numtok(topducks, ',') < totaltop < sc:
            ds = 0
            sc = 0
            continue
        if func.numtok(topducks, ',') == totaltop:
            break
        if func.numtok(topducks, ',') > totaltop:
            break
        scr = func.gettok(datt, ds, ',')
        if int(func.gettok(scr, 0, '?')) == topducklist[sc]:
            if topducks != '':
                topducks = topducks + ',' + func.gettok(datt, ds, ',')
                sc += 1
                ds = 0
            if topducks == '':
                topducks = func.gettok(datt, ds, ',')
                sc += 1
                ds = 0
            continue
        if int(func.gettok(scr, 0, '?')) != topducklist[sc]:
            ds += 1
            continue
        if ds == ntok and func.numtok(topducks, ',') < 5:
            ds = 0
            continue

    # assemble and clean up final top duck score message

    x = 0
    topdmsg = ''
    if totaltop > 5:
        totaltop = 5
    while x <= totaltop:
        if x >= totaltop:
            break
        topd = func.gettok(topducks, x, ',')
        if topdmsg != '':
            usr = func.gettok(topd, 1, '?')
            topdmsg = topdmsg + ' | ' + func.gettok(usr, 1, "'") + ' ' + func.gettok(topd, 0, '?') + ' xp'
            if x == totaltop:
                break
            if x < totaltop:
                x += 1
                continue
        if topdmsg == '':
            usr = func.gettok(topd, 1, '?')
            topdmsg = func.gettok(usr, 1, "'") + ' ' + func.gettok(topd, 0, '?') + ' xp'
            if x == totaltop:
                break
            if x < totaltop:
                x += 1
                continue
    print('TOP DUCKS: ' + str(topdmsg))
    if isconnect:
        irc.send(b'PRIVMSG ' + duckchan + b' :The top ducks are: ' + topdmsg.encode() + b'\r\n')


# ===> topduck

# FUNCTION #============================================================================================================
# Name...........: top_shot
# Description....: manages the shot ducks statistics for daily, weekly, monthly and all time.
# Syntax.........: top_shot()
# Parameters.....: None
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def top_shot():
    global daily
    global weekly
    global monthly
    global totalshot
    global month
    global week
    global day
    daily = func.cnfread('duckhunt.cnf', 'top_shot', 'daily')
    weekly = func.cnfread('duckhunt.cnf', 'top_shot', 'weekly')
    monthly = func.cnfread('duckhunt.cnf', 'top_shot', 'monthly')
    totalshot = func.cnfread('duckhunt.cnf', 'top_shot', 'totalshot')
    month = func.cnfread('duckhunt.cnf', 'top_shot', 't_month')
    week = func.cnfread('duckhunt.cnf', 'top_shot', 't_week')
    day = func.cnfread('duckhunt.cnf', 'top_shot', 't_day')

    current_day = func.gettok(str(date.today()), 2, '-')
    current_week = date.today().isocalendar()[1]
    current_month = func.gettok(str(date.today()), 1, '-')
    if str(current_day) != str(day):
        day = current_day
        func.cnfwrite('duckhunt.cnf', 'top_shot', 't_day', str(day))
        if isconnect is True and duckhunt is True:
            irc.send(b'PRIVMSG ' + duckchan + b' :Total ducks shot for yesterday: ' + bytes(str(daily),
                                                                                            'utf-8') + b' The daily total shots has been reset for a new day!\r\n')
        daily = 0
        func.cnfwrite('duckhunt.cnf', 'top_shot', 'daily', str(daily))
    if str(current_week) != str(week):
        week = current_week
        func.cnfwrite('duckhunt.cnf', 'top_shot', 't_week', str(week))
        if isconnect is True and duckhunt is True:
            irc.send(b'PRIVMSG ' + duckchan + b' :Total ducks shot for last week: ' + bytes(str(weekly),
                                                                                            'utf-8') + b' The weekly total shots has been reset for a new week!\r\n')
        weekly = 0
        func.cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', str(weekly))
    if str(current_month) != str(month):
        month = current_month
        func.cnfwrite('duckhunt.cnf', 'top_shot', 't_month', str(month))
        if isconnect is True and duckhunt is True:
            irc.send(b'PRIVMSG ' + duckchan + b' :Total ducks shot for last month: ' + bytes(str(monthly),
                                                                                             'utf-8') + b' The monthly total shots has been reset for a new week!\r\n')
        monthly = 0
        func.cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', str(monthly))
    return


# ===> top_shot

# ======================================================================================================================
# MAIN LOOP STUFF
# ======================================================================================================================

# ======================================================================================================================
# Connect to server
# ======================================================================================================================
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(b"USER " + botname + b" " + botname + b" " + botname + b" :Super DuckHunt Python Version by Neo_Nemesis\r\n")
irc.send(b"NICK " + botname + b"\r\n")
if str(botpass) != '0':
    irc.send(b'PASS ' + bytes(str(botpass), 'utf-8') + b'\r\n')
# ======================================================================================================================
# main loop - start
# ======================================================================================================================
while 1:
    # if bot gets disocnnect, will attempt to reconnect. Kinda buggy
    if exitvar == 'Disconnect':
        time.sleep(5)
        exitvar = 'Connect'
        irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc.connect((server, port))
        irc.send(
            b"USER " + botname + b" " + botname + b" " + botname + b" :Super DuckHunt Python Version by Neo_Nemesis\r\n")
        irc.send(b"NICK " + botname + b"\r\n")
        if botpass != '0':
            irc.send(b'PASS ' + bytes(str(botpass), 'utf-8') + b'\r\n')
        continue
    # total shots timer
    if isconnect:
        top_shot()
    # IRC stuff
    text = irc.recv(2040)
    txt = text.splitlines()
    x = 0
    for x in range(len(txt)):
        print(b'Data: ' + txt[x])
        data = txt[x].split(b" ")
        # Server ping
        if data[0] == b'PING':
            irc.send(b"PONG " + data[1] + b'\r\n')
            continue
# ======================================================================================================================
# Messages and data
# ======================================================================================================================
        if len(data) > 2:
# ======================================================================================================================
# JOIN channel after MOTD and start duck timer
# ======================================================================================================================
            if data[1] == b'376':
                isconnect = True
                if str(botpass) != '0':
                    irc.send(b'PRIVMSG ' + b'NickServ :IDENTIFY ' + bytes(str(botpass), 'utf-8') + b'\r\n')
                irc.send(b"JOIN " + duckchan + b"\r\n")
                # Start DuckHunt Timer (for ducks only)
                timer_thread = threading.Thread(target=duck_timer)
                timer_thread.start()
# ======================================================================================================================
# /NAMES list - for user list control
# ======================================================================================================================
            if data[1] == b'353':
                ircnamesrf(str(data))

# ======================================================================================================================
# Events handling (Join, mode, part/quit, kick, nick
# Also calls /NAMES whenever user info changes on the channel
# ======================================================================================================================
            # join events
            if data[1] == b'JOIN':
                temp = txt[x].split(b'!')
                username = temp[0].strip(b':')
                if str(username) != str(botname):
                    ircnamesrf('0', 'r')
                    irc.send(b'NAMES ' + duckchan + b'\r\n')
                continue
            # mode events
            if data[1] == b'MODE':
                if data[2].lower() == duckchan:
                    ircnamesrf('0', 'r')
                    irc.send(b'NAMES ' + duckchan + b'\r\n')
                continue
            # part/quit events
            if data[1] == b'PART' or data[1] == b'QUIT':
                temp = txt[x].split(b'!')
                username = temp[0].strip(b':')
                # if bot disconnects, reconnects automatically after 5 seconds
                if str(username) == str(botname) and data[1] == b'QUIT':
                    exitvar = 'Disconnect'
                    isconnect = False
                    continue
                # userlist update
                if str(username) != str(botname) and data[2].lower() == duckchan:
                    ircnamesrf('0', 'r')
                    irc.send(b'NAMES ' + duckchan + b'\r\n')
                continue
            # kick events
            if data[1] == b'KICK':
                # rejoin channel when kicked
                if data[2].lower() == duckchan and data[3] == botname:
                    irc.send(b'JOIN ' + duckchan + b'\r\n')
                    continue
                # user list update
                ircnamesrf('0', 'r')
                irc.send(b'NAMES ' + duckchan + b'\r\n')
                continue
            # nick events
            if data[1] == b'NICK':
                if data[2].lower() == duckchan:
                    ircnamesrf('0', 'r')
                    irc.send(b'NAMES ' + duckchan + b'\r\n')
                    continue
                continue
# ======================================================================================================================
# PRIVMSG stuff (Channel & PM)
# ======================================================================================================================
            if data[1] == b'PRIVMSG':
# ======================================================================================================================
# Flood control here
# ======================================================================================================================

                # flood control activated
                if flood_check is True and flood_cont is True and duckhunt is True:
                    if data[3] == b':!flood':
                        temp = txt[x].split(b'!')
                        username = temp[0].strip(b':')
                        adminlist = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin')
                        botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster')
                        if func.istok(adminlist, username.decode(), ',') is True or func.istok(botmaster,
                                                                                               username.decode(),
                                                                                               ',') is True:
                            flood_time = time.time()
                            flood = 0
                            flood_cont = False
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :\x037* Flood Control Overide by ' + username + b' *\x03\r\n')
                            continue
                    f_time = time.time() - float(flood_timer)
                    if f_time >= 45:
                        flood_time = time.time()
                        flood = 0
                        flood_cont = False
                        irc.send(b'PRIVMSG ' + duckchan + b' :\x033* Flood Control Deactivated *\x03\r\n')
                        continue
                    continue
                # flood control not activated
                elif flood_check is True and flood_cont is False and duckhunt is True and func.cnfexists('duckhunt.cnf',
                                                                                                         'flood_protection',
                                                                                                         str(data[
                                                                                                                 3].decode()).replace(
                                                                                                             ':',
                                                                                                             '')) is True:
                    flood = int(flood) + 1
                    f_time = time.time() - float(flood_time)
                    cmds = func.gettok(func.cnfread('duckhunt.cnf', 'duckhunt', 'floodcheck'), 0, ',')
                    secs = func.gettok(func.cnfread('duckhunt.cnf', 'duckhunt', 'floodcheck'), 1, ',')
                    print('FLOOD COUNT: ' + str(flood) + ' FLOOD TIME: ' + str(f_time))
                    if float(f_time) > float(secs) and int(flood) < int(cmds):
                        flood_time = time.time()
                        flood = 0
                    if int(flood) > int(cmds):
                        f_time = time.time() - float(flood_time)
                        print('FLOOD TIME: ' + str(f_time))
                        if float(f_time) <= float(secs):
                            flood_cont = True
                            flood_timer = time.time()
                            time.sleep(2)
                            irc.send(b'PRIVMSG ' + duckchan + b' :\x034* Flood Control Activated *\x03\r\n')
                            continue
                        if float(f_time) > float(secs):
                            flood_time = time.time()
                            flood = 0
# ======================================================================================================================
# Store requesting username
# ======================================================================================================================
                temp = txt[x].split(b'!')
                username = temp[0].strip(b':')
                bot.iecheck(str(username))
# ======================================================================================================================
# CTCP VERSION, PING, FINGER
# ======================================================================================================================
                if data[2].lower() == botname.lower():
                    if data[3] == b":\x01VERSION\x01":
                        irc.send(
                            b"NOTICE " + username + b' :\x01VERSION Super DuckHunt [Python Bot]: ' + botversion + b' by Neo_Nemesis' + b'\x01\r\n')
                        continue
                    if data[3] == b":\x01FINGER\x01":
                        irc.send(
                            b"NOTICE " + username + b' :\x01FINGER Super DuckHunt [Python Bot]: ' + botversion + b' by Neo_Nemesis' + b'\x01\r\n')
                        continue
                    if data[3] == b":\x01PING":
                        irc.send(b"NOTICE " + username + b' :\x01PING ' + data[4] + b'\r\n')
                        continue
# ======================================================================================================================
# BOTMASTER AND ADMIN CONTROLS (PRIVMSG): /privmsg BotName <command> <parameters>
# ======================================================================================================================

                if data[2].lower() == botname.lower():
                    dusername = username.decode()
# spawnduck <normal/golden> ============================================================================================
#           /privmsg BotName spawnduck <optional: normal/golden> --> spawn a duck
                    if data[3].lower() == b':spawnduck' and duckhunt is True:
                        dusername = username.decode()
                        if func.istok(botmaster, str(dusername), ',') is False and func.istok(adminlist, str(dusername),
                                                                                              ',') is False:
                            continue
                        if len(data) == 4:
                            for x in range(maxducks + 1):
                                if x == 0:
                                    continue
                                d_key = 'd' + str(x)
                                if duck[d_key] == 'None':
                                    spawnduck(d_key, 'normal')
                                    start_time = time.time()
                                    break
                                if x == maxducks:
                                    irc.send(
                                        b'NOTICE ' + username + b' :The maximum amount of ducks are currently spawned.\r\n')
                                    break
                                continue
                        if len(data) == 5:
                            if data[4].lower() == b'normal':
                                for x in range(maxducks + 1):
                                    if x == 0:
                                        continue
                                    d_key = 'd' + str(x)
                                    if duck[d_key] == 'None':
                                        spawnduck(d_key, 'normal')
                                        start_time = time.time()
                                        break
                                    if x == maxducks:
                                        irc.send(
                                            b'NOTICE ' + username + b' :The maximum amount of ducks are currently spawned.\r\n')
                                        break
                                    continue
                            if data[4].lower() == b'golden':
                                for x in range(maxducks + 1):
                                    if x == 0:
                                        continue
                                    d_key = 'd' + str(x)
                                    if duck[d_key] == 'None':
                                        spawnduck(d_key, 'gold')
                                        start_time = time.time()
                                        break
                                    if x == maxducks:
                                        irc.send(
                                            b'NOTICE ' + username + b' :The maximum amount of ducks are current spawned.\r\n')
                                        break
                                    continue
                        continue
# del <admin/ignore/botmaster> <username> ==============================================================================
#           /privmsg botname del <admin/ignore/botmaster> <username> --> remove username
                    if data[3].lower() == b':del':
                        dusername = username.decode()
                        if func.istok(botmaster, str(dusername), ',') is False and func.istok(adminlist, str(dusername),
                                                                                              ',') is False:
                            continue
                        if len(data) <= 4:
                            continue
                        # del admin <username>
                        if data[4].lower() == b'admin' and len(data) == 6 and func.istok(botmaster, str(dusername),
                                                                                         ',') is True:
                            data5 = data[5].decode()
                            adminlist = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin')
                            if adminlist == '0' or func.istok(adminlist, str(data5), ',') == False:
                                irc.send(b'NOTICE ' + username + b' :Invalid request: User "' + bytes(str(data5), 'utf-8') + b'" does not exist in the admin list.\r\n')
                                continue
                            if func.numtok(adminlist, ',') == 1:
                                adminlist = '0'
                            if func.numtok(adminlist, ',') > 1:
                                adminlist = func.deltok(adminlist, str(data5), ',')
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'admin', str(adminlist))
                            irc.send(b'NOTICE ' + username + b' :User ' + bytes(str(data5), 'utf-8') + b' removed from the admin list.\r\n')
                            continue
                        # del botmaster <username>
                        if data[4].lower() == b'botmaster' and len(data) == 6 and func.istok(botmaster, str(dusername),
                                                                                             ',') is True:
                            data5 = data[5].decode()
                            botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster')
                            if func.numtok(botmaster, ',') == 1:
                                irc.send(
                                    b'NOTICE ' + username + b' :Invalid request: There must always be at least 1 botmaster.\r\n')
                                continue
                            botmaster = func.deltok(botmaster, str(data5), ',')
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'botmaster', botmaster)
                            irc.send(b'NOTICE ' + username + b' :User ' + bytes(str(data5), 'utf-8') + b' removed from the botmaster list.\r\n')
                            continue
                        # del ignore <username>
                        if data[4].lower() == b'ignore' and len(data) == 6:
                            data5 = data[5].decode()
                            botignore = func.cnfread('duckhunt.cnf', 'duckhunt', 'ignore')
                            if botignore == '0' or func.istok(botignore, str(data5), ',') == False:
                                irc.send(b'NOTICE ' + username + b' :Invalid request: User "' + bytes(str(data5),
                                                                                                      'utf-8') + b'" does not exist in the ignore list.\r\n')
                                continue
                            if func.numtok(botignore, ',') == 1:
                                botignore = '0'
                            if func.numtok(botignore, ',') > 1:
                                botignore = func.deltok(botignore, str(data5), ',')
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'ignore', botignore)
                            irc.send(b'NOTICE ' + username + b' :User ' + bytes(str(data5),
                                                                                'utf-8') + b' removed from the ignore list.\r\n')
                            continue
                        continue
# add <admin/ignore/botmaster> <username> ==============================================================================
#           /privmsg BotName add <admin/ignore/botmaster> <username> - Add username
                    if data[3].lower() == b':add':
                        dusername = username.decode()
                        if func.istok(botmaster, str(dusername), ',') == False and func.istok(adminlist, str(dusername),
                                                                                              ',') == False:
                            continue
                        if len(data) <= 4:
                            continue
                        # add admin <username>
                        if data[4].lower() == b'admin' and len(data) == 6 and func.istok(botmaster, str(dusername),
                                                                                         ',') is True:
                            adminlist = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin')
                            data5 = data[5].decode()
                            if func.istok(adminlist, data5, ',') is True:
                                irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5),
                                                                               'utf-8') + b' is already in the admin list.\r\n')
                                continue
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'admin') != '0':
                                adminlist = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin')
                                adminlist = func.addtok(adminlist, str(data5), ',')
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'admin') == '0':
                                adminlist = str(data5)
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'admin', adminlist)
                            irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5),
                                                                           'utf-8') + b' has been added to the admin list.\r\n')
                            continue
                        # add botmaster <username>
                        if data[4].lower() == b'botmaster' and len(data) == 6 and func.istok(botmaster, str(dusername),
                                                                                             ',') is True:
                            botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster')
                            data5 = data[5].decode()
                            if func.istok(botmaster, data5, ',') is True:
                                irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5),
                                                                               'utf-8') + b' is already in the botmaster list.\r\n')
                                continue
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster') != '0':
                                botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster')
                                botmaster = func.addtok(botmaster, str(data5), ',')
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster') == '0':
                                botmaster = str(data5)
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'botmaster', botmaster)
                            irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5),
                                                                           'utf-8') + b' has been added to the botmaster list.\r\n')
                            continue
                        # add ignore <username>
                        if data[4].lower() == b'ignore' and len(data) == 6:
                            botignore = func.cnfread('duckhunt.cnf', 'duckhunt', 'ignore')
                            data5 = data[5].decode()
                            if func.istok(botignore, data5, ',') is True:
                                irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5),
                                                                               'utf-8') + b' is already in the ignore list.\r\n')
                                continue
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'ignore') != '0':
                                botignore = func.cnfread('duckhunt.cnf', 'duckhunt', 'ignore')
                                botignore = func.addtok(botignore, str(data5), ',')
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'ignore') == '0':
                                botignore = str(data5)
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'ignore', botignore)
                            irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5),
                                                                           'utf-8') + b' has been added to the ignore list.\r\n')
                            continue
                        continue
# set <maxducks/spawntime/flytime/duckexp/duckfear/duckgold/friendrate/gunricochet> <value> ============================
#           /privmsg BotName set <maxducks/spawntime/flytime/duckexp/duckfear/duckgold/friendrate/gunricochet> <value>
# this sets the specified object to the specified value
# EXAMPLE: /privmsg BotName set maxducks 5
# - sets the maximum amount of duck spawns to 5
# (1 - 5 ducks total, don't go over 5 --> recommend 3 - 4)
# ==========================================================
                    if data[3].lower() == b':set':
                        if func.istok(botmaster, str(dusername), ',') == False:
                            continue
                        if len(data) <= 4:
                            continue
                        # set maxducks N
                        if data[4].lower() == b'maxducks' and len(data) == 6:
                            data5 = data[5].decode()
                            if data5.isnumeric() == False or isinstance(data5, float) is True:
                                irc.send(
                                    b'NOTICE ' + username + b' :Invalid request: "maxducks" value must be an integer.\r\n')
                                continue
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'maxducks', str(data5))
                            if duckhunt:
                                irc.send(
                                    b'NOTICE ' + username + b' :The maxducks setting has been changed to: ' + bytes(
                                        str(data5), 'utf-8') + b' ducks.\r\n')
                                if duck_exists():
                                    irc.send(
                                        b'NOTICE ' + duckchan + b" :Due to a parameter change, the ducks in the area have flown away.     \x0314\xc2\xb7\xc2\xb0'`'\xc2\xb0-.,\xc2\xb8\xc2\xb8.\xc2\xb7\xc2\xb0'`\r\n")
                            maxducks = int(data5)
                            for x in range(maxducks + 1):
                                if x == 0:
                                    continue
                                duck_key = 'd' + str(x)
                                duck[duck_key] = 'None'
                                continue
                            continue
                        # set spawntime N
                        if data[4].lower() == b'spawntime' and len(data) == 6:
                            data5 = data[5].decode()
                            if data5.isnumeric() is False or isinstance(data5, float) is True:
                                irc.send(
                                    b' NOTICE ' + username + b' :Invalid request: "spawntime" value must be an integer.\r\n')
                                continue
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'spawntime', str(data5))
                            irc.send(b'NOTICE ' + username + b' :The spawntime setting has been changed to: ' + bytes(
                                str(data5), 'utf-8') + b' seconds.\r\n')
                            spawntime = int(data5)
                            continue
                        # set flyimte N
                        if data[4].lower() == b'flytime' and len(data) == 6:
                            data5 = data[5].decode()
                            if data5.isnumeric() is False or isinstance(data5, float) is True:
                                irc.send(
                                    b'NOTICE ' + username + b' :Invalid request: "flytime" value must be an integer.\r\n')
                                continue
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'flytime', str(data5))
                            irc.send(b'NOTICE ' + username + b' :The flytime setting has been changed to: ' + bytes(
                                str(data5), 'utf-8') + b' seconds.\r\n')
                            flytime = int(data5)
                            continue
                        # set duckexp N
                        if data[4].lower() == b'duckexp' and len(data) == 6:
                            data5 = data[5].decode()
                            if data5.isnumeric() is False or isinstance(str(data5), float) is True:
                                irc.send(
                                    b'NOTICE ' + username + b' :Invalid request: The "duckexp" value must be an integer.\r\n')
                                continue
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'duckexp', str(data5))
                            irc.send(b'NOTICE ' + username + b' :The duckexp setting has been changed to: ' + bytes(
                                str(data5), 'utf-8') + b' xp.\r\n')
                            duckexp = int(data5)
                            continue
                        # set duckfear N
                        if data[4].lower() == b'duckfear' and len(data) == 6:
                            data5 = data[5].decode()
                            if data5.isnumeric() is False or isinstance(str(data5), float) is True:
                                irc.send(
                                    b'NOTICE ' + username + b' :Invalid request: The "duckfear" value must be an integer.\r\n')
                                continue
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'duckfear', str(data5))
                            irc.send(b'NOTICE ' + username + b' :The duckfear setting has been changed to: ' + bytes(
                                str(data5), 'utf-8') + b' points.\r\n')
                            duckfear = int(data5)
                            continue
                        # set duckgold N
                        if data[4].lower() == b'duckgold' and len(data) == 6:
                            data5 = data[5].decode()
                            if data5.isnumeric() is False or isinstance(str(data5), float) is True:
                                irc.send(
                                    b'NOTICE ' + username + b' :Invalid request: The "duckgold" value must be an integer.\r\n')
                                continue
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'duckgold', str(data5))
                            irc.send(b'NOTICE ' + username + b' :The duckgold setting has been changed to: ' + bytes(
                                str(data5), 'utf-8') + b'%.\r\n')
                            duckgold = int(data5)
                            continue
                        # set friendrate N
                        if data[4].lower() == b'friendrate' and len(data) == 6:
                            data5 = data[5].decode()
                            if data5.isnumeric() is False or isinstance(str(data5), float) is True:
                                irc.send(
                                    b'NOTICE ' + username + b' :Invalid request: The "friendrate" value must be an integer.\r\n')
                                continue
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'friendrate', str(data5))
                            irc.send(b'NOTICE ' + username + b' :The friendrate setting has been changed to: ' + bytes(
                                str(data5), 'utf-8') + b'%.\r\n')
                            friendrate = int(data5)
                            continue
                        # set gunricochet N
                        if data[4].lower() == b'gunricochet' and len(data) == 6:
                            data5 = data[5].decode()
                            if data5.isnumeric() is False or isinstance(str(data5), float) is True:
                                irc.send(
                                    b'NOTICE ' + username + b' :Invalid request: The "gunricochet" value must be an integer.\r\n')
                                continue
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'gunricochet', str(data5))
                            irc.send(b'NOTICE ' + username + b' :The gunricochet setting has been changed to: ' + bytes(
                                str(data5), 'utf-8') + b'%.\r\n')
                            gunricochet = int(data5)
                            continue
                        # set flood <on/off> <msg,time>
                        # /privmsg BotName set flood on 45,46
                        # /privmsg BotName set flood off
                        if data[4].lower() == b'flood' and len(data) >= 4:
                            if len(data) == 4:
                                flc = func.cnfread('duckhunt.cnf', 'duckhunt', 'floodcheck')
                                if flc == '0':
                                    irc.send(
                                        b'NOTICE ' + username + b' :The flood protection is currently disabled.\r\n')
                                    continue
                                if flc != '0':
                                    cmds = func.gettok(str(data[6].decode()), 0, ',')
                                    secs = func.gettok(str(data[6].decode()), 1, ',')
                                    irc.send(
                                        b'NOTICE ' + username + b' :The current flood protection settings are: ' + bytes(
                                            str(cmds), 'utf-8') + b'requests in: ' + bytes(str(secs),
                                                                                           'utf-8') + b' seconds.\r\n')
                                    continue

                            if data[5].lower() == b'on' and len(data) == 7 and func.numtok(data[6], ',') == 2:
                                func.cnfwrite('duckhunt.cnf', 'duckhunt', 'floodcheck', str(data[6].decode()))
                                flood_check = True
                                cmds = func.gettok(str(data[6].decode()), 0, ',')
                                secs = func.gettok(str(data[6].decode()), 1, ',')
                                irc.send(
                                    b'NOTICE ' + username + b' :The flood protection settings have been changed to: ' + bytes(
                                        str(cmds), 'utf-8') + b'requests in: ' + bytes(str(secs),
                                                                                       'utf-8') + b' seconds.\r\n')
                                continue
                            if data[5].lower() == b'off':
                                flood_check = False
                                func.cnfwrite('duckhunt.cnf', 'duckhunt', 'floodcheck', '0')
                                irc.send(b'NOTICE ' + username + b' :The flood protection has been disabled.\r\n')
                                continue
                        continue
# ======================================================================================================================
# Botmaster and Admin CHANNEL COMMANDS * *
# ======================================================================================================================

                if data[2].lower() == duckchan and bot.isaccess(username.decode()) is True:

# ======================================================================================================================
# !exit (botmaster only)
# ======================================================================================================================
                    if data[3].lower() == b":!exit":
                        dusername = username.decode()
                        if func.istok(botmaster, str(dusername), ',') == False:
                            continue
                        irc.send(b"PRIVMSG " + duckchan + b" :Shutting down...\r\n")
                        time.sleep(1)
                        irc.send(b"QUIT :Super DuckHunt Bot by Neo_Nemesis\r\n")
                        exitvar = True
                        exit()
# ======================================================================================================================
# !duckhunt <on/off> (Botmaster and Admin only)
# ======================================================================================================================
                    if data[3].lower() == b':!duckhunt' and len(data) == 5:
                        dusername = username.decode()
                        if func.istok(botmaster, str(dusername), ',') == False and func.istok(adminlist, str(dusername),
                                                                                              ',') == False:
                            continue
                        if data[4].lower() == b'on':
                            if duckhunt:
                                irc.send(b'PRIVMSG ' + duckchan + b' :Super DuckHunt is already turned on.\r\n')
                                continue
                            elif not duckhunt:
                                duckhunt = True
                                irc.send(b'PRIVMSG ' + duckchan + b' :Super DuckHunt has been turned on.\r\n')
                                continue
                        if data[4].lower() == b'off':
                            if not duckhunt:
                                irc.send(b'PRIVMSG ' + duckchan + b' :Super DuckHunt is already turned off.\r\n')
                                continue
                            elif duckhunt:
                                duckhunt = False
                                irc.send(b'PRIVMSG ' + duckchan + b' :Super DuckHunt has been turned off.\r\n')
                                continue
                        continue
# ======================================================================================================================
# User - CHANNEL COMMANDS *
# ======================================================================================================================

                if data[2].lower() == duckchan and duckhunt is True:

# ======================================================================================================================
# !shop [id] [target]
# shop purchases are controlled here
# ======================================================================================================================
                    if data[3].lower() == b':!shop':
                        if func.cnfexists('duckhunt.cnf', 'ducks', str(username).lower()) == False:
                            irc.send(
                                b'NOTICE ' + username + b" :You can't use the shop yet because you haven't played. Shoot some ducks first.\r\n")
                            continue
                        if len(data) == 4:
                            shopmenu(username)
                            continue
                        if len(data) >= 5:
                            data4 = data[4].decode()
                            if not data4.isnumeric():
                                continue
                            itemid = int(data[4])
                            # data prep
                            ammo = bot.duckinfo(username, b'ammo')
                            rounds = func.gettok(ammo, 0, '?')
                            mags = func.gettok(ammo, 1, '?')
                            mrounds = func.gettok(ammo, 2, '?')
                            mmags = func.gettok(ammo, 3, '?')
                            xp = bot.duckinfo(username, b'xp')
                            # inventory = bot.duckinfo(username, b'inv') - No longer used
                            gunstats = bot.duckinfo(username, b'guninfo')
                            accuracy = func.gettok(gunstats, 0, '?')
                            reliability = func.gettok(gunstats, 1, '?')
                            mreliability = func.gettok(gunstats, 2, '?')
                            # effects = bot.duckinfo(username, b'effects') - No longer used
                            breadbox = bot.duckinfo(username, b'bread')
                            bread = func.gettok(breadbox, 0, '?')
                            mbread = func.gettok(breadbox, 1, '?')
# not enough xp to purchase ============================================================================================
                            if int(xp) < bot.shopprice(username, itemid):
                                irc.send(b'NOTICE ' + username + b' :You do not have enough xp for this.\r\n')
                                continue
# checks if user is on the channel, and prevents users from targeting themselves =======================================
                            if len(data) == 6:
                                if int(itemid) == 14 or int(itemid) == 15 or int(itemid) == 16 or int(itemid) == 17:
                                    # can't use it on the bot
                                    if str(data[5]) == str(botname):
                                        irc.send(b'NOTICE ' + username + b' :Nice try ;-)\r\n')
                                        continue
                                    # user isn't on the channel
                                    if namecheck(str(data[5])) == False:
                                        irc.send(
                                            b'NOTICE ' + username + b' :' + data[5] + b' is not in the channel.\r\n')
                                        continue
                                    # user hasn't played yet
                                    if func.cnfexists('duckhunt.cnf', 'ducks', str(data[5].lower())) == False:
                                        irc.send(b'NOTICE ' + username + b' :' + data[5] + b" hasn't played yet.\r\n")
                                        continue
                                    # can't use it on yourself
                                    if str(data[5].lower()) == str(username.lower()):
                                        irc.send(b'NOTICE ' + username + b" :Don't do that to yourself!\r\n")
                                        continue
# 1 - single bullet ====================================================================================================
                            if int(itemid) == 1:
                                # can't hold any more
                                if rounds == mrounds:
                                    irc.send(b'NOTICE ' + username + b' :You cannot carry any more bullets.\r\n')
                                    continue
                                # shop purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # apply ammo
                                rounds = int(rounds) + 1
                                ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
                                bot.duckinfo(username, b'ammo', str(ammo))
                                # confirmation
                                irc.send(b'NOTICE ' + username + b' :You purchased a single bullet.\r\n')
                                continue
# 2 - refill magazine ==================================================================================================
                            if int(itemid) == 2:
                                # can't hold anymore
                                if mags == mmags:
                                    irc.send(b'NOTICE ' + username + b' :All your magazines are full.\r\n')
                                    continue
                                # shop purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # apply refill
                                mags = int(mags) + 1
                                ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
                                bot.duckinfo(username, b'ammo', str(ammo))
                                # confirmation
                                irc.send(b'NOTICE ' + username + b' :You refilled 1 magazine.\r\n')
                                continue
# 3 - gun grease =======================================================================================================
                            if int(itemid) == 3:
                                bot.data_check(str(username), 'gun_grease', )
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'gun_grease', str(username)) is True:
                                    # 24 hour timer calculation
                                    timeleft = bot.data_check(str(username.lower()), 'gun_grease', 'get')
                                    print(timeleft)
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    irc.send(
                                        b'NOTICE ' + username + b' :You already own Gun Grease. [Time Remaining: ' + bytes(
                                            str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # shop purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'gun_grease', str(username), str(time.time()))
                                # purchase confirmation
                                irc.send(
                                    b'NOTICE ' + username + b' :You purchased Gun Grease. Gun reliability will decrease at a lower rate for 24 hours.\r\n')
                                continue
# 4 - magazine upgrade =================================================================================================
                            if int(itemid) == 4:
                                # magazines cannot be upgraded any further (max upgrade already reached)
                                if int(mrounds) == 12:
                                    irc.send(
                                        b'NOTICE ' + username + b' :Your magazines are already fully upgraded, and cannot be upgraded further.\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # apply upgrade
                                mrounds = int(mrounds) + 1
                                ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
                                bot.duckinfo(username, b'ammo', str(ammo))
                                # confirmation
                                irc.send(
                                    b'NOTICE ' + username + b' :You upgraded your magazines! They can now hold ' + bytes(
                                        str(mrounds), 'utf-8') + b' rounds.\r\n')
                                continue
# 5 - return confiscated gun ===========================================================================================
                            if int(itemid) == 5:
                                # not confiscated
                                if confiscatedguns == '':
                                    irc.send(b'NOTICE ' + username + b' :Your gun is not currently confiscated.\r\n')
                                    continue
                                if func.istok(confiscatedguns, str(username), ',') == False:
                                    irc.send(b'NOTICE ' + username + b' :Your gun is not currently confiscated.\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # remove confiscation
                                if confiscatedguns == str(username):
                                    confiscatedguns = ''
                                if func.istok(confiscatedguns, str(username), ','):
                                    confiscatedguns = func.deltok(confiscatedguns, str(username), ',')
                                # confirmation
                                irc.send(b'NOTICE ' + username + b' :Your confiscated gun has been returned.\r\n')
                                irc.send(
                                    b'PRIVMSG ' + duckchan + b' :\x01ACTION returns ' + username + b"'s gun to them.\x01\r\n")
                                continue
# 6 - gun cleaning =====================================================================================================
                            if int(itemid) == 6:
                                # gun doesn't need to be cleaned
                                if reliability == mreliability:
                                    irc.send(b'NOTICE ' + username + b" :Your gun doesn't need to be cleaned.\r\n")
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # apply reliability restore
                                reliability = mreliability
                                gunstats = accuracy + '?' + reliability + '?' + mreliability
                                bot.duckinfo(username, b'guninfo', str(gunstats))
                                # confirmation
                                irc.send(
                                    b'NOTICE ' + username + b" :Your gun is now cleaned and reliability is restored to maximum.\r\n")
                                continue
# 7 - gun upgrade ======================================================================================================
                            if int(itemid) == 7:
                                # can't upgrade anymore/fully upgraded
                                if str(accuracy) == '100' and str(mreliability) == '100':
                                    irc.send(b'NOTICE ' + username + b' :Your gun is already fully upgraded.\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # apply upgrade
                                if int(accuracy) < 100:
                                    accuracy = int(accuracy) + 5
                                if int(mreliability) < 100:
                                    mreliability = int(mreliability) + 5
                                    reliability = mreliability
                                gunstats = str(accuracy) + '?' + str(reliability) + '?' + str(mreliability)
                                bot.duckinfo(username, b'guninfo', gunstats)
                                # confirmation
                                irc.send(
                                    b'NOTICE ' + username + b' :You have upgraded your gun. Accuracy and reliability have increased.\r\n')
                                continue
# 8 - Gun Lock =====================================================================================================
                            if int(itemid) == 8:
                                bot.data_check(username, 'trigger_lock')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'trigger_lock', str(username)) == True:
                                    # 24 hour timer calculation
                                    timeleft = bot.data_check(str(username), 'trigger_lock', 'get')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    irc.send(b'NOTICE ' + username + b' :You already own Gun Lock. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                if int(itemid) == 8:
                                    xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'trigger_lock', str(username), str(time.time()))
                                # purchase confirmation
                                irc.send(b'NOTICE ' + username + b' :You purchased Gun Lock. Gun will only fire when a duck is present, preventing some confiscations and accidents for 24 hours.\r\n')
                                continue
# 9 - silencer =========================================================================================================
                            if int(itemid) == 9:
                                bot.data_check(username, 'silencer')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'silencer', str(username)) == True:
                                    # 24 hour timer calculation
                                    timeleft = bot.data_check(str(username), 'silencer', 'get')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    irc.send(
                                        b'NOTICE ' + username + b' :You already own Silencer. [Time Remaining: ' + bytes(
                                            str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'silencer', str(username), str(time.time()))
                                # purchase confirmation
                                irc.send(
                                    b'NOTICE ' + username + b' :You purchased a Silencer for your gun. You will not scare away ducks for 24 hours.\r\n')
                                continue
# 10 - lucky charm =====================================================================================================
                            if int(itemid) == 10:
                                bot.data_check(username, 'lucky_charm')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)) == True:
                                    # 24 hour timer calculation
                                    timeleft = bot.data_check(str(username), 'lucky_charm', 'get')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    irc.send(
                                        b'NOTICE ' + username + b' :You already own Lucky Charm. [Time Remaining: ' + bytes(
                                            str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'lucky_charm', str(username), str(time.time()))
                                # purchase confirmation
                                irc.send(
                                    b'NOTICE ' + username + b' :You purchased a Lucky Charm. You will earn douple xp 24 hours.\r\n')
                                continue
# 11 - sunglasses ======================================================================================================
                            if int(itemid) == 11:
                                bot.data_check(username, 'sunglasses')
                                bot.data_check(username, 'bedazzled')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'sunglasses', str(username)) == True:
                                    # 24 hour timer calculation
                                    timeleft = bot.data_check(str(username), 'sunglasses', 'get')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    irc.send(
                                        b'NOTICE ' + username + b' :You already own Sunglasses. [Time Remaining: ' + bytes(
                                            str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # cannot buy sunglasses if currently bedazzled.
                                if func.cnfexists('duckhunt.cnf', 'bedazzled', str(username)) == True:
                                    # add 1 hour timer stuff
                                    timeleft = bot.data_check(str(username), 'bedazzled', 'get')
                                    timemath = func.hour1() - math.ceil(time.time() - float(timeleft))
                                    timemath = bot.timeconvertmsg(timemath)
                                    irc.send(
                                        b'NOTICE ' + username + b' :You are currently bedazzled and have to wait for it to wear off to use Sunglasses. [Time Remaining: ' + bytes(
                                            str(timemath), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'sunglasses', str(username), str(time.time()))
                                # purchase confirmation
                                irc.send(
                                    b'NOTICE ' + username + b' :You purchased Sunglasses. You are protected from bedazzlement for 24 hours.\r\n')
                                continue
# 12 - dry clothes =====================================================================================================
                            if int(itemid) == 12:
                                bot.data_check(username, 'soggy')
                                # not soggy
                                if func.cnfexists('duckhunt.cnf', 'soggy', str(username)) == False:
                                    irc.send(b'NOTICE ' + username + b' :Your clothes are already dry.\r\n')
                                    continue
                                # remove soggy
                                func.cnfdelete('duckhunt.cnf', 'soggy', str(username))
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                irc.send(
                                    b'NOTICE ' + username + b' :You purchased Dry Clothes. You are no longer soggy.\r\n')
                                continue
# 13 - additional magazine =============================================================================================
                            if int(itemid) == 13:
                                # can't carry any more
                                if int(mmags) == 5:
                                    irc.send(
                                        b'NOTICE ' + username + b' :You cannot carry anymore additional magazines.\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                mmags = int(mmags) + 1
                                ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
                                bot.duckinfo(username, b'ammo', str(ammo))
                                irc.send(
                                    b'NOTICE ' + username + b' :You purchased an additional magainze, you can now carry ' + bytes(
                                        str(mmags), 'utf-8') + b' magazines.\r\n')
                                continue
# 14 - mirror ==========================================================================================================
                            if int(itemid) == 14 and len(data) == 6:
                                bot.data_check(data[5], 'bedazzled')
                                bot.data_check(data[5], 'sunglasses')
                                # target already bedazzled
                                teffects = bot.duckinfo(data[5], b'effects')
                                tinventory = bot.duckinfo(data[5], b'inv')
                                if func.cnfexists('duckhunt.cnf', 'bedazzled', str(data[5])) == True:
                                    irc.send(b'NOTICE ' + username + b' :' + data[5] + b' is already bedazzled.\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # target wearing sunglasses!
                                if func.cnfexists('duckhunt.cnf', 'sunglasses', str(data[5])) == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Bedazzles ' + data[
                                        5] + b', with a mirror, but ' + data[
                                                 5] + b' is wearing sunglasses so the mirror has no effect.\r\n')
                                    continue
                                # target not wearing sunglasses
                                if func.cnfexists('duckhunt.cnf', 'sunglasses', str(data[5])) == False:
                                    # adding time entry (1 hours)
                                    func.cnfwrite('duckhunt.cnf', 'bedazzled', str(data[5]), str(time.time()))
                                    # confirmation
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Bedazzles ' + data[
                                        5] + b' with a mirror who is now blinded for 1 hour.\r\n')
                                    continue
# 15 - handful of sand =================================================================================================
                            if int(itemid) == 15 and len(data) == 6:
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # reliability reduction
                                tgunstats = bot.duckinfo(data[5], b'guninfo')
                                taccuracy = func.gettok(tgunstats, 0, '?')
                                treliability = func.gettok(tgunstats, 1, '?')
                                tmreliability = func.gettok(tgunstats, 2, '?')
                                # effects - apply
                                if float(treliability) < 20:
                                    treliability = 0
                                if float(treliability) >= 20:
                                    treliability = float(treliability) - 5
                                tgunstats = str(taccuracy) + '?' + str(treliability) + '?' + str(tmreliability)
                                bot.duckinfo(data[5], b'guninfo', str(tgunstats))
                                # confirmation
                                irc.send(
                                    b'PRIVMSG ' + duckchan + b' :' + username + b' > Pours a handful of sand into ' +
                                    data[5] + b"'s gun, reducing its reliability by 5%.\r\n")
                                continue
# 16 - water bucket ====================================================================================================
                            if int(itemid) == 16 and len(data) == 6:
                                bot.data_check(data[5], 'soggy')
                                bot.data_check(data[5], 'rain_coat')
                                # target is already soggy
                                if func.cnfexists('duckhunt.cnf', 'soggy', str(data[5])) == True:
                                    irc.send(b'NOTICE ' + username + b' :' + data[5] + b' is already soggy.\r\n')
                                    continue
                                # target has a rain coat
                                if func.cnfexists('duckhunt.cnf', 'rain_coat', str(data[5])) == True:
                                    # purchase
                                    xp = int(xp) - bot.shopprice(username, itemid)
                                    bot.duckinfo(username, b'xp', str(xp))
                                    irc.send(
                                        b'PRIVMSG ' + duckchan + b' :' + username + b' > Dumps a bucket of water on ' +
                                        data[5] + b', but thanks to a rain coat, ' + data[
                                            5] + b' is protected from being soggy.\r\n')
                                    continue
                                # target not wearing a rain coat
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'soggy', str(data[5]), str(time.time()))
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # confirmation
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Dumps a bucket of water on ' +
                                         data[5] + b'. ' + data[5] + b' is now soggy for 1 hour.\r\n')
                                continue
# 17 - sabotage ========================================================================================================
                            if int(itemid) == 17 and len(data) == 6:
                                # target already sabotaged
                                teffects = bot.duckinfo(data[5], b'effects')
                                if func.cnfexists('duckhunt.cnf', 'sabotage', str(data[5])) == True:
                                    irc.send(
                                        b'NOTICE ' + username + b' :' + data[5] + b"'s gun is already sabotaged.\r\n")
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # target effects apply - lasts 1 shot
                                func.cnfwrite('duckhunt.cnf', 'sabotage', str(data[5]), str(True))
                                # confirmation
                                irc.send(
                                    b'PRIVMSG ' + duckchan + b' :' + username + b' > Sabotages the gun while ' + data[
                                        5] + b" isn't looking.\r\n")
                                continue
# 18 - accident insurance ==============================================================================================
                            if int(itemid) == 18:
                                bot.data_check(username, 'accident_insurance')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)) == True:
                                    # 24 hour timer calculation
                                    timeleft = bot.data_check(str(username), 'accident_insurance', 'get')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    irc.send(
                                        b'NOTICE ' + username + b' :You already own Accident Insurance. [Time Remaining: ' + bytes(
                                            str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'accident_insurance', str(username), str(time.time()))
                                # confirmation
                                irc.send(
                                    b'NOTICE ' + username + b' :You purchased Accident Insurance. This will prevent gun confiscation for 24 hours.\r\n')
                                continue
# 19 - bread - "ammo" for befriending ducks ============================================================================
                            if int(itemid) == 19:
                                # bread box is not empty
                                if int(bread) > 0:
                                    irc.send(
                                        b'NOTICE ' + username + b" :You can't purchase more bread until your bread box is empty.\r\n")
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # apply bread refill
                                bread = mbread
                                breadbox = bread + '?' + mbread
                                bot.duckinfo(username, b'bread', str(breadbox))
                                # confirmation
                                irc.send(b'NOTICE ' + username + b' :You purchased a loaf of bread.\r\n')
                                continue
# 20 - rain coat - prevents soggy and duck bombing =====================================================================
                            if int(itemid) == 20:
                                bot.data_check(username, 'soggy')
                                bot.data_check(username, 'rain_coat')
                                # currently soggy
                                if func.cnfexists('duckhunt.cnf', 'soggy', str(username)) == True:
                                    # 1 hour timer calculation
                                    timeleft = bot.data_check(username, 'soggy', 'get')
                                    timemath = func.hour1() - math.ceil(time.time() - float(timeleft))
                                    timemath = bot.timeconvertmsg(timemath)
                                    irc.send(
                                        b'NOTICE ' + username + b' :You are currently soggy and cannot purchase Rain Coat until you are dry. [Time Remaining: ' + bytes(
                                            str(timemath), 'utf-8') + b']\r\n')
                                    continue
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'rain_coat', str(username)) == True:
                                    # 24 hour timer calculation
                                    timeleft = bot.data_check(str(username), 'rain_coat', 'get')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    irc.send(
                                        b'NOTICE ' + username + b' :You already own Rain Coat. [Time Remaining: ' + bytes(
                                            str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'rain_coat', str(username), str(time.time()))
                                irc.send(
                                    b'NOTICE ' + username + b' :You purchased Rain Coat. This will protect against water buckets and duck bombs for 24 hours.\r\n')
                                continue
                            # end of shop
                            continue
# ======================================================================================================================
# !bomb - duck bombing run (requires 50+ befriended ducks, once every 24 hours)
# ======================================================================================================================
                    if data[3].lower() == b':!bomb' and len(data) == 5:
                        if func.cnfexists('duckhunt.cnf', 'ducks', str(username.lower())) == False:
                            irc.send(b'NOTICE ' + username + b' :You have not played yet.\r\n')
                            continue
                        friend = bot.duckinfo(str(username.lower()), b'friend')
                        # can't bomb the bot
                        if str(data[4].lower()) == str(botname.lower()):
                            irc.send(b'NOTICE ' + username + b' :Nice try ;-)\r\n')
                            continue
                        # not enough duck friends/no player stats
                        if int(friend) < 50:
                            irc.send(b'NOTICE ' + username + b' :You do not have enough duck friends to do this, you need at least 50 befriended ducks.\r\n')
                            continue
                        # user isn't on the channel
                        if not namecheck(str(data[4].decode())):
                            irc.send(b'NOTICE ' + username + b' :' + data[4] + b' is not in the channel.\r\n')
                            continue
                        # user hasn't played yet
                        if not func.cnfexists('duckhunt.cnf', 'ducks', str(data[4].lower())):
                            irc.send(b'NOTICE ' + username + b' :' + data[4] + b" hasn't played yet.\r\n")
                            continue
                        # can't bomb yourself
                        if str(data[4].lower()) == str(username.lower()):
                            irc.send(b'NOTICE ' + username + b" :Don't do that to yourself!\r\n")
                            continue
                        bot.data_check(str(username), 'duck_bomb')
                        # check if user has done duck bombing in last 24 hours
                        if func.cnfexists('duckhunt.cnf', 'duck_bomb', str(username)):
                            timeleft = bot.data_check(str(username), 'duck_bomb', 'get')
                            timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                            timeval = bot.timeconvertmsg(timemath)
                            irc.send(b'NOTICE ' + username + b" :You've recently used a duck bombing within the last 24 hours. Try again in: " + bytes(str(timeval), 'utf-8') + b'\r\n')
                            continue
                        bot.data_check(str(data[4].decode()), 'soggy')
                        # target is already soggy
                        if func.cnfexists('duckhunt.cnf', 'soggy', str(data[4])) == True:
                            irc.send(b'NOTICE ' + username + b' :' + bytes(str(data[4].decode()), 'utf-8') + b' is already soggy.\r\n')
                            continue
                        # user has not used duck bombing in the last 24 hours
                        func.cnfwrite('duckhunt.cnf', 'duck_bomb', str(username), str(time.time()))
                        bot.data_check(data[4], 'rain_coat')
                        # target is wearing raincoat
                        if func.cnfexists('duckhunt.cnf', 'rain_coat', str(data[4])) == True:
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b' > Calls in a duck bombing, a fleet of ' + bytes(
                                    str(friend),
                                    'utf-8') + b' duck friends, flying in formation, swoop down and drop duck bombs on ' +
                                data[4] + b', but thanks to a rain coat, the bombing has no effect!\r\n')
                            continue
                        # target is not wearing raincoat
                        if func.cnfexists('duckhunt.cnf', 'rain_coat', str(data[4])) == False:
                            # target 1 hour timer set
                            func.cnfwrite('duckhunt.cnf', 'soggy', str(data[4]), str(time.time()))
                            # commence bombing
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b' > Calls in a duck bombing, a fleet of ' + bytes(
                                    str(friend),
                                    'utf-8') + b' duck friends, flying in formation, swoop down and drop duck bombs on ' +
                                data[4] + b'! Making ' + data[4] + b' soggy for 1 hour.\r\n')
                            continue
                        continue
# ======================================================================================================================
# !lastduck
# ======================================================================================================================
                    if data[3].lower() == b':!lastduck':
                        last_time = time.time() - float(start_time)
                        mesg = bot.timeconvertmsg(last_time)
                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > The last duck was seen: ' + bytes(
                            str(mesg), 'utf-8') + b' ago.\r\n')
                        continue
# ======================================================================================================================
# !topduck
# ======================================================================================================================
                    if data[3].lower() == b':!topduck':
                        topduck()
                        continue
# ======================================================================================================================
# !duckstats <optional user name>
# ======================================================================================================================
                    if data[3].lower() == b':!duckstats':
                        if len(data) == 4:
                            duckstats(username, username)
                            continue
                        if len(data) == 5:
                            duckstats(username, data[4])
                            continue
# ======================================================================================================================
# !rearm <all, optional user name>
# !rearm - rearms yourself.
# Channel OPs/Bot Access/Bot Master only
# ======================================================================================================================
                    if data[3].lower() == b':!rearm':
                        dusername = username.decode()
                        if func.istok(botmaster, str(dusername), ',') == False and func.istok(adminlist, str(dusername),
                                                                                              ',') == False:
                            continue
                        # !rearm
                        if len(data) == 4:
                            if func.istok(confiscatedguns, str(username), ',') == False:
                                irc.send(
                                    b'PRIVMSG ' + duckchan + b' :' + username + b' > Your gun is not confiscated.\r\n')
                                continue
                            if func.numtok(confiscatedguns, ',') == 1:
                                confiscatedguns = ''
                            if func.numtok(confiscatedguns, ',') > 1:
                                confiscatedguns = func.deltok(confiscatedguns, str(username), ',')
                            irc.send(b'PRIVMSG ' + duckchan + b' :\x01ACTION returns ' + username + b"'s gun.\x01\r\n")
                            continue
                        # !rearm <username> and !rearm all
                        if len(data) == 5:
                            if data[4] == b'all':
                                confiscatedguns = ''
                                irc.send(
                                    b'PRIVMSG ' + duckchan + b' :\x01ACTION returns all confiscated guns to the hunters.\x01\r\n')
                                continue
                            if func.istok(confiscatedguns, str(data[4]), ',') == False:
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + data[4] + b"'s gun is not confiscated.\r\n")
                                continue
                            if func.numtok(confiscatedguns, ',') == 1:
                                confiscatedguns = ''
                            if func.numtok(confiscatedguns, ',') > 1:
                                confiscatedguns = func.deltok(confiscatedguns, str(username), ',')
                            irc.send(b'PRIVMSG ' + duckchan + b' :\x01ACTION returns ' + data[
                                4] + b"'s gun.\x01\r\n")
                            continue
# ======================================================================================================================
# !reload
# ======================================================================================================================
                    if data[3].lower() == b':!reload':
                        # check if players gun is confiscated
                        if func.istok(confiscatedguns, str(username), ',') == True:
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x034You are not armed.\x03\r\n')
                            continue
                        # unjam gun
                        if func.istok(jammedguns, str(username), ',') == True:
                            if func.numtok(jammedguns, ',') == 1:
                                jammedguns = ''
                            if func.numtok(jammedguns, ',') > 1:
                                jammedguns = func.deltok(jammedguns, str(username), ',')
                            func.cnfwrite('duckhunt.cnf', 'duck_jam', str(username), '0')
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b" > \x0314*Crr..CLICK*\x03     You unjam your gun.\r\n")
                            continue
                        # new users with no stats, gun doesn't need to be reloaded
                        if func.cnfexists('duckhunt.cnf', 'ducks', str(username)) == False:
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b" > Your gun doesn't need to be reloaded. | Rounds: 7/7 | Magazines: 3/3\r\n")
                            continue
                        # reloading gun
                        rounds = func.gettok(bot.duckinfo(username, b'ammo'), 0, '?')
                        mags = func.gettok(bot.duckinfo(username, b'ammo'), 1, '?')
                        mrounds = func.gettok(bot.duckinfo(username, b'ammo'), 2, '?')
                        mmags = func.gettok(bot.duckinfo(username, b'ammo'), 3, '?')
                        if int(rounds) == 0:
                            # out of magazines
                            if int(mags) == 0:
                                irc.send(
                                    b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034You are out of magazines.\x03 | Rounds:\x034 0\x03/" + mrounds.encode() + b" | Magazines:\x034 0\x03/" + mmags.encode() + b'\r\n')
                                continue
                            # successful reload
                            mags = int(mags) - 1
                            mags = str(mags)
                            rounds = mrounds
                            ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
                            bot.duckinfo(username, b'ammo', ammo)
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b" > \x0314*CLACK CLACK*\x03     You reload. | Rounds: " + rounds.encode() + b'/' + mrounds.encode() + b' | Magazines: ' + mags.encode() + b'/' + mmags.encode() + b'\r\n')
                            continue
                        # gun doesn't need to be reloaded
                        if int(rounds) > 0:
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b" > Your gun doesn't need to be reloaded. | Rounds: " + rounds.encode() + b'/' + mrounds.encode() + b' | Magazines: ' + mags.encode() + b'/' + mmags.encode() + b'\r\n')
                            continue
# ======================================================================================================================
# !bang (this entire section will be recoded for update 1.1)
# ======================================================================================================================
                    if data[3].lower() == b":!bang":
                        # check if players gun is confiscated
                        if func.istok(confiscatedguns, str(username), ','):
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x034You are not armed.\x03\r\n')
                            continue
                        # new users with no stats, assigns stats
                        if not func.cnfexists('duckhunt.cnf', 'ducks', str(username)):
                            func.cnfwrite('duckhunt.cnf', 'ducks', 'cache', '1')
                            dinfo = '7?3?7?3,0,0,0,1,200,0,0,75?80?80,0,0,12?12,0'
                            func.cnfwrite('duckhunt.cnf', 'ducks', str(username), str(dinfo))
                        # shooting data
                        dinfo = func.cnfread('duckhunt.cnf', 'ducks', str(username))
                        ammo = func.gettok(dinfo, 0, ',')
                        rounds = func.gettok(ammo, 0, '?')  # .encode()
                        mags = func.gettok(ammo, 1, '?')  # .encode()
                        mrounds = func.gettok(ammo, 2, '?')  # .encode()
                        mmags = func.gettok(ammo, 3, '?')  # .encode()
                        guninfo = func.gettok(dinfo, 8, ',')
                        accuracy = func.gettok(guninfo, 0, '?')  # .encode()
                        reliability = func.gettok(guninfo, 1, '?')  # .encode()
                        mreliability = func.gettok(guninfo, 2, '?')  # .encode()
                        xp = bot.duckinfo(username, b'xp')
                        best = bot.duckinfo(username, b'best')
                        ducks = bot.duckinfo(username, b'ducks')
                        gducks = bot.duckinfo(username, b'gducks')
                        accidents = bot.duckinfo(username, b'accidents')
                        # inventory = bot.duckinfo(username, b'inv') # No longer used
                        # effects = bot.duckinfo(username, b'effects') # no longer used
                        levelup = bot.duckinfo(username, b'levelup')
                        bot.data_check(username, 'soggy')
                        # checks if player is soggy
                        if func.cnfexists('duckhunt.cnf', 'soggy', str(username)):
                            # determine time remaining
                            # 1 hour timer calculation
                            timeleft = bot.data_check(str(username), 'soggy', 'get')
                            timemath = func.hour1() - math.ceil(time.time() - float(timeleft))
                            timemath = bot.timeconvertmsg(timemath)
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034Your clothes are all soggy. You cannot hunt until you're dry. \x033[Time Remaining: " + bytes(
                                    str(timemath), 'utf-8') + b']\x03\r\n')
                            continue
                        # checks if player is sabotaged
                        if func.cnfexists('duckhunt.cnf', 'sabotage', str(username)):
                            func.cnfdelete('duckhunt.cnf', 'sabotage', str(username))
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*CLICK PFFFFT*\x03     \x034Your gun was sabotaged.\x03\r\n')
                            continue
                        # Gun Lock
                        if func.cnfexists('duckhunt.cnf', 'trigger_lock', str(username)) is True and duck_exists() is False:
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*CLICK*\x03    \x034GUN LOCKED\x03\r\n')
                            continue
                        # empty magazine
                        if int(rounds) == 0:
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*CLICK*\x03     \x034EMPTY MAGAZINE\x03 | Rounds:\x034 ' + rounds.encode() + b'\x03/' + mrounds.encode() + b' | Magazines: ' + mags.encode() + b'/' + mmags.encode() + b'\r\n')
                            continue
                        # gun needs service (guns jam excessively under 60)
                        if float(reliability) <= 60:
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*CLICK-CLACK*\x03     \x034Your gun is too dirty and needs to be cleaned...\x03\r\n')
                            continue
                        # jammed gun
                        if not func.cnfexists('duckhunt.cnf', 'duck_jam', str(username)):
                            jammed = random.randint(1, 100)
                            if jammed >= float(reliability) or func.istok(jammedguns, str(username), ',') == True:
                                # jammed
                                if jammedguns == b'':
                                    jammed = str(username)
                                else:
                                    jammedguns = str(jammedguns) + ',' + str(username)
                                irc.send(
                                    b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*CLACK*\x03     \x034Your gun is jammed, you must reload to unjam it...\x03\r\n')
                                continue
                        if func.cnfexists('duckhunt.cnf', 'duck_jam', str(username)):
                            func.cnfdelete('duckhunt.cnf', 'duck_jam', str(username))
                        # fired a round
                        rounds = int(rounds) - 1
                        bot.data_check(username, 'gun_grease')
                        # does not have gun grease
                        if not func.cnfexists('duckhunt.cnf', 'gun_grease', str(username)):
                            reliability = float(reliability) - 0.1
                        # has gun grease
                        if func.cnfexists('duckhunt.cnf', 'gun_grease', str(username)):
                            reliability = float(reliability) - 0.01
                        reliability = round(reliability, 2)
                        ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
                        guninfo = str(accuracy) + '?' + str(reliability) + '?' + str(mreliability)
                        bot.duckinfo(username, b'ammo', ammo)
                        bot.duckinfo(username, b'guninfo', guninfo)
                        duckexists = duck_exists()
                        # no duck in the area...
                        if not duckexists:
                            # determines ricochet
                            ricochet = random.randint(1, 100)
                            # bullet ricochets
                            if int(ricochet) <= int(gunricochet):
                                damage = ''
                                dmg = random.randint(1, 3)
                                if dmg == 1:
                                    damage = 'strikes a distant window!'
                                if dmg == 2:
                                    damage = 'strikes another hunter!'
                                if dmg == 3:
                                    damage = 'starts a wildfire!'
                                # xp deduction
                                if int(xp) <= dmg:
                                    xp = 0
                                if int(xp) > dmg:
                                    xp = int(xp) - dmg
                                bot.duckinfo(username, b'xp', str(xp))
                                # accident
                                accidents = int(accidents) + 1
                                bot.duckinfo(username, b'accidents', str(accidents))
                                bot.data_check(username.lower(), 'accident_insurance')
                                # does not have accident insurance
                                if not func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username.lower())):
                                    if confiscatedguns != '':
                                        confiscatedguns = str(confiscatedguns) + ',' + str(username)
                                    if confiscatedguns == '':
                                        confiscatedguns = str(username)
                                    irc.send(
                                        b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(
                                            str(damage), 'utf-8') + b' \x034[-' + str(
                                            dmg).encode() + b' xp] [GUN CONFISCATED: Ricochet]\x03\r\n')
                                    continue
                                # has accident insurance
                                if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username.lower())):
                                    irc.send(
                                        b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(
                                            str(damage), 'utf-8') + b' \x034[-' + str(
                                            dmg).encode() + b' xp]\x03 \x033[GUN NOT CONFISCATED: Accident Insurance]\x03\r\n')
                                    continue
                            # damage determination
                            damage = ''
                            dmg = random.randint(1, 3)
                            if dmg == 1:
                                damage = 'Shot a distant window!'
                            if dmg == 2:
                                damage = 'Shot another hunter!'
                            if dmg == 3:
                                damage = 'Wildfire!'
                            # xp deduction
                            if int(xp) <= dmg:
                                xp = 0
                            if int(xp) > dmg:
                                xp = int(xp) - dmg
                            bot.duckinfo(username, b'xp', str(xp))
                            # accident
                            accidents = int(accidents) + 1
                            bot.duckinfo(username, b'accidents', str(accidents))
                            bot.data_check(username.lower(), 'accident_insurance')
                            # does not have accident insurance
                            if not func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username.lower())):
                                if confiscatedguns != '':
                                    confiscatedguns = str(confiscatedguns) + ',' + str(username)
                                if confiscatedguns == '':
                                    confiscatedguns = str(username)
                                irc.send(
                                    b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03    What did you shoot at? There is no duck in the area...   \x034[-' + str(
                                        dmg).encode() + b' xp] [GUN CONFISCATED: ' + damage.encode() + b']\x03\r\n')
                                continue
                            # has accident insurance
                            if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username.lower())):
                                irc.send(
                                    b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03    What did you shoot at? There is no duck in the area...    \x034[-' + str(
                                        dmg).encode() + b' xp]\x03 \x033[GUN NOT CONFISCATED: Accident Insurance]\x03\r\n')
                                continue
                        # duck exists
                        if duckexists:
                            bot.data_check(username, 'bedazzled')
                            # check if bedazzled
                            if func.cnfexists('duckhunt.cnf', 'bedazzled', str(username)):
                                bot.duckinfo(username, b'xp', str(xp))
                                bot.data_check(username, 'accident_insurance')
                                # has accident insurance - no confiscation
                                if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                    # xp deduction, -1 xp
                                    if int(xp) <= 1:
                                        xp = 0
                                    if int(xp) > 1:
                                        xp = int(xp) - 1
                                    bot.duckinfo(username, b'xp', str(xp))
                                    irc.send(
                                        b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x034     Missed due to being bedazzled. [-1 xp] \x033[GUN NOT CONFISCATED: Accident Insurance]\x03\r\n')
                                    continue
                                # does not have accident insurance - confiscation
                                if not func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                    # apply confiscation
                                    if confiscatedguns != '':
                                        confiscatedguns = str(confiscatedguns) + ',' + str(username)
                                    if confiscatedguns == '':
                                        confiscatedguns = str(username)
                                    # damage determination
                                    damage = ''
                                    dmg = random.randint(1, 3)
                                    if dmg == 1:
                                        damage = 'Shot a distant window!'
                                    if dmg == 2:
                                        damage = 'Shot another hunter!'
                                    if dmg == 3:
                                        damage = 'Wildfire!'
                                    # xp deduction
                                    if int(xp) <= dmg:
                                        xp = 0
                                    if int(xp) > dmg:
                                        xp = int(xp) - dmg
                                    bot.duckinfo(username, b'xp', str(xp))
                                    irc.send(
                                        b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x034     Missed due to being debazzled. [-' + str(
                                            dmg).encode() + b' xp] [GUN CONFISCATED: ' + damage.encode() + b']\x03\r\n')
                                    continue
                            dk = 1
                            duckdata = ''
                            duck_time = ''
                            while dk <= maxducks:
                                duckid = 'd' + str(dk)
                                if duck[duckid] == 'None':
                                    dk += 1
                                    continue
                                if duck[duckid] != 'None':
                                    duckdata = duck[duckid]
                                    duck_time = func.gettok(duckdata, 0, ',')
                                    break
                            # duck fear management
                            bot.data_check(username, 'silencer')
                            if fear_factor >= duckfear and func.cnfexists('duckhunt.cnf', 'silencer',
                                                                          str(username)) == False:
                                fl = 1
                                while fl <= maxducks:
                                    # duckid = 'duck' + str(fl)
                                    # func.cnfwrite('duckhunt.cnf', 'duck_data', duckid, 'None')
                                    duckid = 'd' + str(fl)
                                    duck[duckid] = 'None'
                                    fl += 1
                                    continue
                                irc.send(
                                    b'PRIVMSG ' + duckchan + b" :\x034Frightened by so much noise, all ducks in the area have fled.\x03     \x0314\xc2\xb7\xc2\xb0'`'\xc2\xb0-.,\xc2\xb8\xc2\xb8.\xc2\xb7\xc2\xb0'`\r\n")
                                fear_factor = False
                                gold_factor = False
                                continue
                            if fear_factor < duckfear and func.cnfexists('duckhunt.cnf', 'silencer',
                                                                         str(username)) == False:
                                scare = random.randrange(2, 8, 1)
                                fear_factor = fear_factor + scare
                            # ======================================================================================================================
                            # !bang - Golden Ducks (this entire section will be recoded for update 1.1)
                            # (hit or miss)
                            # ======================================================================================================================
                            if func.gettok(duckdata, 1, ',') == 'golden':
                                # determine if hit or miss (golden ducks have same as normal ducks, but take 3-4 hits.)
                                hitormiss = random.randrange(0, 120, 1)
                                # successful hit
                                if hitormiss <= int(accuracy):
                                    duckhp = func.gettok(duckdata, 2, ',')
                                    # shot down the golden duck
                                    if int(duckhp) == 0:
                                        # duck count statistics

                                        # reaction time determination
                                        reacttime = round(time.time() - float(duck_time), 2)
                                        if best == '0':
                                            # best = reacttime
                                            bot.duckinfo(username, b'best', str(reacttime))
                                        if float(best) > reacttime:
                                            # best = reacttime
                                            bot.duckinfo(username, b'best', str(reacttime))
                                        # increase golden ducks
                                        gducks = int(gducks) + 1
                                        bot.duckinfo(username, b'gducks', str(gducks))
                                        # increase xp (golden ducks are triple exp)
                                        exp = duckexp * 3
                                        bot.data_check(username, 'lucky_charm')
                                        # does not have lucky charm
                                        # if func.istok(inventory, 'Lucky Charm', '?') == False:
                                        if not func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                            # top shot counter
                                            daily = int(daily) + 1
                                            func.cnfwrite('duckhunt.cnf', 'top_shot', 'daily', str(daily))
                                            weekly = int(weekly) + 1
                                            func.cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', str(weekly))
                                            monthly = int(monthly) + 1
                                            func.cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', str(monthly))
                                            totalshot = int(totalshot) + 1
                                            func.cnfwrite('duckhunt.cnf', 'top_shot', 'totalshot', str(totalshot))
                                            # xp addition
                                            xp = int(xp) + exp
                                            bot.duckinfo(username, b'xp', str(xp))
                                            # confiscated guns returned silently after duck is shot
                                            confiscatedguns = ''
                                            irc.send(
                                                b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     you shot down the GOLDEN DUCK in ' + bytes(
                                                    str(reacttime),
                                                    'utf-8') + b' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + bytes(
                                                    str(exp), 'utf-8') + b' xp] [TOTAL GOLDEN DUCKS: ' + bytes(
                                                    str(gducks), 'utf-8') + b']\x03\r\n')
                                            # func.cnfwrite('duckhunt.cnf', 'duck_data', duckid, 'None')
                                            duck[duckid] = 'None'
                                            start_time = time.time()
                                            if not duck_exists():
                                                fear_factor = False
                                            # check for level up
                                            if int(xp) >= int(levelup):
                                                level_up(username)
                                            continue
                                        # has lucky charm
                                        # if func.istok(inventory, 'Lucky Charm', '?') == True:
                                        if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                            # top shot counter
                                            daily = int(daily) + 1
                                            func.cnfwrite('duckhunt.cnf', 'top_shot', 'daily', str(daily))
                                            weekly = int(weekly) + 1
                                            func.cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', str(weekly))
                                            monthly = int(monthly) + 1
                                            func.cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', str(monthly))
                                            totalshot = int(totalshot) + 1
                                            func.cnfwrite('duckhunt.cnf', 'top_shot', 'totalshot', str(totalshot))
                                            # xp addition
                                            exp = exp * 2
                                            xp = int(xp) + exp
                                            bot.duckinfo(username, b'xp', str(xp))
                                            # confiscated guns returned silently after duck is shot
                                            confiscatedguns = ''
                                            irc.send(
                                                b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     you shot down the GOLDEN DUCK in ' + bytes(
                                                    str(reacttime),
                                                    'utf-8') + b' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + bytes(
                                                    str(exp),
                                                    'utf-8') + b' xp - Lucky Charm] [TOTAL GOLDEN DUCKS: ' + bytes(
                                                    str(gducks), 'utf-8') + b']\x03\r\n')
                                            # func.cnfwrite('duckhunt.cnf', 'duck_data', duckid, 'None')
                                            duck[duckid] = 'None'
                                            start_time = time.time()
                                            if not duck_exists():
                                                fear_factor = False
                                            # check for level up
                                            if int(xp) >= int(levelup):
                                                level_up(username)
                                            continue
                                    # the duck surivived (life -1)
                                    if int(duckhp) > 0:
                                        duckhp = int(duckhp) - 1
                                        duckdata = func.gettok(duckdata, 0, ',') + ',' + func.gettok(duckdata, 1,
                                                                                                     ',') + ',' + str(
                                            duckhp)
                                        duck[duckid] = duckdata
                                        irc.send(
                                            b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     The Golden Duck surivived!     \x02\x034\\_O< [Life -1]\r\n')
                                        continue
                                # missed
                                if hitormiss > int(accuracy):
                                    ricochet = random.randrange(1, 100, 1)
                                    # bullet ricochets
                                    if int(ricochet) <= int(gunricochet):
                                        damage = ''
                                        dmg = random.randint(1, 3)
                                        if dmg == 1:
                                            damage = 'strikes a distant window!'
                                        if dmg == 2:
                                            damage = 'strikes another hunter!'
                                        if dmg == 3:
                                            damage = 'starts a wildfire!'
                                        # xp deduction
                                        if int(xp) <= dmg:
                                            xp = 0
                                        if int(xp) > dmg:
                                            xp = int(xp) - dmg
                                        bot.duckinfo(username, b'xp', str(xp))
                                        # accident
                                        accidents = int(accidents) + 1
                                        bot.duckinfo(username, b'accidents', str(accidents))
                                        bot.data_check(username, 'accident_insurance')
                                        # does not have accident insurance
                                        if not func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                            if confiscatedguns != '':
                                                confiscatedguns = str(confiscatedguns) + ',' + str(username)
                                            if confiscatedguns == '':
                                                confiscatedguns = str(username)
                                            irc.send(
                                                b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(
                                                    str(damage), 'utf-8') + b' \x034[-' + str(
                                                    dmg).encode() + b' xp] [GUN CONFISCATED: Ricochet]\x03\r\n')
                                            continue
                                        # has accident insurance
                                        if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                            irc.send(
                                                b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(
                                                    str(damage), 'utf-8') + b' \x034[-' + str(
                                                    dmg).encode() + b' xp]\x03 \x033[GUN NOT CONFISCATED: Accident Insurance]\x03\r\n')
                                            continue
                                    # xp deduction (-3 for golden ducks)
                                    if int(xp) <= 3:
                                        xp = 0
                                    if int(xp) > 3:
                                        xp = int(xp) - 3
                                    bot.duckinfo(username, b'xp', str(xp))
                                    irc.send(
                                        b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03     \x034MISSED   [-3 xp]\x03\r\n')
                                    continue
                            # ======================================================================================================================
                            # !bang - Normal Ducks that have ability to turn golden (this entire section will be recoded for update 1.1)
                            # (hit or miss)
                            # ======================================================================================================================
                            if func.gettok(duckdata, 1, ',') == 'gold':
                                # determine if hit or miss (possible golden ducks are harder to hit)
                                hitormiss = random.randrange(50, 225, 1)
                                # successful hit (same as normal duck)
                                if hitormiss <= int(accuracy):
                                    # reaction time determination
                                    reacttime = round(time.time() - float(duck_time), 2)
                                    if best == '0':
                                        bot.duckinfo(username, b'best', str(reacttime))
                                    if float(best) > reacttime:
                                        bot.duckinfo(username, b'best', str(reacttime))
                                    # increase ducks
                                    ducks = int(ducks) + 1
                                    bot.duckinfo(username, b'ducks', str(ducks))
                                    bot.data_check(username, 'lucky_charm')
                                    # does not have lucky charm
                                    if not func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                        # top shot counter
                                        daily = int(daily) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'daily', str(daily))
                                        weekly = int(weekly) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', str(weekly))
                                        monthly = int(monthly) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', str(monthly))
                                        totalshot = int(totalshot) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'totalshot', str(totalshot))
                                        # increase xp
                                        xp = int(xp) + duckexp
                                        bot.duckinfo(username, b'xp', str(xp))
                                        # confiscated guns returned silently after duck is shot
                                        confiscatedguns = ''
                                        irc.send(
                                            b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     you shot down the duck in ' + bytes(
                                                str(reacttime),
                                                'utf-8') + b' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + bytes(
                                                str(duckexp), 'utf-8') + b' xp] [TOTAL DUCKS: ' + bytes(str(ducks),
                                                                                                        'utf-8') + b']\x03\r\n')
                                        duck[duckid] = 'None'
                                        start_time = time.time()
                                        if duck_exists() == False:
                                            fear_factor = False
                                        # check for level up
                                        if int(xp) >= int(levelup):
                                            level_up(username)
                                        continue
                                    # has lucky charm
                                    if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                        # top shot counter
                                        daily = int(daily) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'daily', str(daily))
                                        weekly = int(weekly) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', str(weekly))
                                        monthly = int(monthly) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', str(monthly))
                                        totalshot = int(totalshot) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'totalshot', str(totalshot))
                                        # increase xp
                                        exp = duckexp * 2
                                        xp = int(xp) + exp
                                        bot.duckinfo(username, b'xp', str(xp))
                                        # confiscated guns returned silently after duck is shot
                                        confiscatedguns = ''
                                        irc.send(
                                            b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     you shot down the duck in ' + bytes(
                                                str(reacttime),
                                                'utf-8') + b' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + bytes(
                                                str(exp), 'utf-8') + b' xp - Lucky Charm] [TOTAL DUCKS: ' + bytes(
                                                str(ducks), 'utf-8') + b']\x03\r\n')
                                        duck[duckid] = 'None'
                                        start_time = time.time()
                                        if duck_exists() == False:
                                            fear_factor = False
                                        # check for level up
                                        if int(xp) >= int(levelup):
                                            level_up(username)
                                        continue
                                # missed (increases chances of duck turning golden, after 3 misses, duck transforms)
                                if hitormiss > int(accuracy):
                                    ricochet = random.randrange(1, 100, 1)
                                    # bullet ricochets
                                    if int(ricochet) <= int(gunricochet):
                                        damage = ''
                                        dmg = random.randint(1, 3)
                                        if dmg == 1:
                                            damage = 'strikes a distant window!'
                                        if dmg == 2:
                                            damage = 'strikes another hunter!'
                                        if dmg == 3:
                                            damage = 'starts a wildfire!'
                                        # xp deduction
                                        if int(xp) <= dmg:
                                            xp = 0
                                        if int(xp) > dmg:
                                            xp = int(xp) - dmg
                                        bot.duckinfo(username, b'xp', str(xp))
                                        # accident
                                        accidents = int(accidents) + 1
                                        bot.duckinfo(username, b'accidents', str(accidents))
                                        bot.data_check(username, 'accident_insurance')
                                        # does not have accident insurance
                                        if not func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                            if confiscatedguns != '':
                                                confiscatedguns = str(confiscatedguns) + ',' + str(username)
                                            if confiscatedguns == '':
                                                confiscatedguns = str(username)
                                            irc.send(
                                                b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(
                                                    str(damage), 'utf-8') + b' \x034[-' + str(
                                                    dmg).encode() + b' xp] [GUN CONFISCATED: Ricochet]\x03\r\n')
                                            continue
                                        # has accident insurance
                                        if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                            irc.send(
                                                b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(
                                                    str(damage), 'utf-8') + b' \x034[-' + str(
                                                    dmg).encode() + b' xp]\x03 \x033[GUN NOT CONFISCATED: Accident Insurance]\x03\r\n')
                                            continue
                                    # xp deduction (-1 for normal/gold ability ducks)
                                    if int(xp) <= 1:
                                        xp = 0
                                    if int(xp) > 1:
                                        xp = int(xp) - 1
                                    bot.duckinfo(username, b'xp', str(xp))
                                    # determine if duck will turn golden
                                    if func.numtok(duckdata, ',') > 2:
                                        # after 3 misses, duck turns golden
                                        goldenratio = random.randint(2, 3)
                                        if int(func.gettok(duckdata, 2, ',')) >= int(goldenratio):
                                            duckstat = random.randrange(2, 3, 1)
                                            duckdata = func.gettok(duckdata, 0, ',') + ',golden,' + str(duckstat)
                                            duck[duckid] = duckdata
                                            irc.send(
                                                b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03     \x034MISSED   [-1 xp]\x037   \x02\\_O<    * GOLDEN DUCK DETECTED *\x02\x03\r\n')
                                            continue
                                        # under 3 misses, not golden yet
                                        if int(func.gettok(duckdata, 2, ',')) < int(goldenratio):
                                            duckstat = int(func.gettok(duckdata, 2, ',')) + 1
                                            duckdata = func.gettok(duckdata, 0, ',') + ',' + func.gettok(duckdata, 1,
                                                                                                         ',') + ',' + str(
                                                duckstat)
                                            duck[duckid] = duckdata
                                            irc.send(
                                                b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03     \x034MISSED   [-1 xp]\x03\r\n')
                                            continue
                                    if func.numtok(duckdata, ',') == 2:
                                        duckdata = duckdata + ",1"
                                        # func.cnfwrite('duckhunt.cnf', 'duck_data', duckid, duckdata)
                                        duck[duckid] = duckdata
                                        irc.send(
                                            b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03     \x034MISSED   [-1 xp]\x03\r\n')
                                        continue
                            # ======================================================================================================================
                            # !bang - Normal Ducks (no ability to turn golden) (this entire section will be recoded for update 1.1)
                            # (hit or miss)
                            # ======================================================================================================================
                            if func.gettok(duckdata, 1, ',') == 'normal':
                                # determine if hit or miss
                                hitormiss = random.randrange(0, 100, 1)
                                # successful hit
                                if hitormiss <= int(accuracy):
                                    # reaction time determination
                                    reacttime = round(time.time() - float(duck_time), 2)
                                    if best == '0':
                                        bot.duckinfo(username, b'best', str(reacttime))
                                    if float(best) > reacttime:
                                        bot.duckinfo(username, b'best', str(reacttime))
                                    # increase ducks
                                    ducks = int(ducks) + 1
                                    bot.duckinfo(username, b'ducks', str(ducks))
                                    bot.data_check(username, 'lucky_charm')
                                    # does not have lucky charm
                                    if not func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                        # top shot counter
                                        daily = int(daily) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'daily', str(daily))
                                        weekly = int(weekly) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', str(weekly))
                                        monthly = int(monthly) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', str(monthly))
                                        totalshot = int(totalshot) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'totalshot', str(totalshot))
                                        # increase xp
                                        xp = int(xp) + duckexp
                                        bot.duckinfo(username, b'xp', str(xp))
                                        # confiscated guns returned silently after duck is shot
                                        confiscatedguns = ''
                                        irc.send(
                                            b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     you shot down the duck in ' + bytes(
                                                str(reacttime),
                                                'utf-8') + b' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + bytes(
                                                str(duckexp), 'utf-8') + b' xp] [TOTAL DUCKS: ' + bytes(str(ducks),
                                                                                                        'utf-8') + b']\x03\r\n')
                                        duck[duckid] = 'None'
                                        start_time = time.time()
                                        if duck_exists() == False:
                                            fear_factor = False
                                        # check for level up
                                        if int(xp) >= int(levelup):
                                            level_up(username)
                                        continue
                                    # has lucky charm
                                    if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)) == True:
                                        # top shot counter
                                        daily = int(daily) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'daily', str(daily))
                                        weekly = int(weekly) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', str(weekly))
                                        monthly = int(monthly) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', str(monthly))
                                        totalshot = int(totalshot) + 1
                                        func.cnfwrite('duckhunt.cnf', 'top_shot', 'totalshot', str(totalshot))
                                        # increase xp
                                        exp = duckexp * 2
                                        xp = int(xp) + exp
                                        bot.duckinfo(username, b'xp', str(xp))
                                        # confiscated guns returned silently after duck is shot
                                        confiscatedguns = ''
                                        irc.send(
                                            b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     you shot down the duck in ' + bytes(
                                                str(reacttime),
                                                'utf-8') + b' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + bytes(
                                                str(exp), 'utf-8') + b' xp - Lucky Charm] [TOTAL DUCKS: ' + bytes(
                                                str(ducks), 'utf-8') + b']\x03\r\n')
                                        duck[duckid] = 'None'
                                        start_time = time.time()
                                        if duck_exists() == False:
                                            fear_factor = False
                                        # check for level up
                                        if int(xp) >= int(levelup):
                                            level_up(username)
                                        continue
                                # missed
                                if hitormiss > int(accuracy):
                                    ricochet = random.randrange(1, 100, 1)
                                    # bullet ricochets
                                    if int(ricochet) <= int(gunricochet):
                                        damage = ''
                                        dmg = random.randint(1, 3)
                                        if dmg == 1:
                                            damage = 'strikes a distant window!'
                                        if dmg == 2:
                                            damage = 'strikes another hunter!'
                                        if dmg == 3:
                                            damage = 'starts a wildfire!'
                                        # xp deduction
                                        if int(xp) <= dmg:
                                            xp = 0
                                        if int(xp) > dmg:
                                            xp = int(xp) - dmg
                                        bot.duckinfo(username, b'xp', str(xp))
                                        # accident
                                        accidents = int(accidents) + 1
                                        bot.duckinfo(username, b'accidents', str(accidents))
                                        bot.data_check(username, 'accident_insurance')
                                        # does not have accident insurance
                                        if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)) == False:
                                            if confiscatedguns != '':
                                                confiscatedguns = str(confiscatedguns) + ',' + str(username)
                                            if confiscatedguns == '':
                                                confiscatedguns = str(username)
                                            irc.send(
                                                b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(
                                                    str(damage), 'utf-8') + b' \x034[-' + str(
                                                    dmg).encode() + b' xp] [GUN CONFISCATED: Ricochet]\x03\r\n')
                                            continue
                                        # has accident insurance
                                        if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)) == True:
                                            irc.send(
                                                b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(
                                                    str(damage), 'utf-8') + b' \x034[-' + str(
                                                    dmg).encode() + b' xp]\x03 \x033[GUN NOT CONFISCATED: Accident Insurance]\x03\r\n')
                                            continue
                                    # xp deduction (-1 for normal ducks)
                                    if int(xp) <= 3:
                                        xp = 0
                                    if int(xp) > 3:
                                        xp = int(xp) - 3
                                    bot.duckinfo(username, b'xp', str(xp))
                                    irc.send(
                                        b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03     \x034MISSED   [-1 xp]\x03\r\n')
                                    continue
                    # ======================================================================================================================
                    # !bef (befriending ducks) (this entire section will be recoded for update 1.1)
                    # ======================================================================================================================
                    if data[3].lower() == b':!bef':
                        # new users with no stats, assigns stats
                        if func.cnfexists('duckhunt.cnf', 'ducks', str(username)) == False:
                            dinfo = '7?3?7?3,0,0,0,1,200,0,0,75?85?85,0,0,12?12,0'
                            func.cnfwrite('duckhunt.cnf', 'ducks', str(username), str(dinfo))
                        # friending data
                        xp = bot.duckinfo(username, b'xp')
                        breadbox = bot.duckinfo(username, b'bread')
                        bread = func.gettok(breadbox, 0, '?')
                        mbread = func.gettok(breadbox, 1, '?')
                        friend = bot.duckinfo(username, b'friend')
                        inventory = bot.duckinfo(username, b'inv')
                        levelup = bot.duckinfo(username, b'levelup')
                        # out of bread
                        if int(bread) == 0:
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034You're out of bread.\x03 \x033[BREAD BOX:\x03\x034 " + bytes(
                                    str(bread), 'utf-8') + b'\x03\x033/' + bytes(str(mbread), 'utf-8') + b']\x03\r\n')
                            continue
                        # tosses a peice of bread
                        bread = int(bread) - 1
                        bot.duckinfo(username, b'bread', str(bread) + '?' + str(mbread))
                        # no duck in the area
                        if duck_exists() == False:
                            irc.send(
                                b'PRIVMSG ' + duckchan + b' :' + username + b' > Tosses a piece of bread at nothing? There are no ducks in the area. \x033[BREAD BOX: ' + bytes(
                                    str(bread), 'utf-8') + b'/' + bytes(str(mbread), 'utf-8') + b']\x03\r\n')
                            continue
                        # duck exists
                        if duck_exists() == True:
                            duckdata = ''
                            dk = 1
                            while dk <= maxducks:
                                duckid = 'd' + str(dk)
                                if duck[duckid] == 'None':
                                    dk += 1
                                    continue
                                if duck[duckid] != 'None':
                                    duckdata = duck[duckid]
                                    duck_time = func.gettok(duckdata, 0, ',')
                                    break
                            # ======================================================================================================================
                            # !bef - normal/gold ability ducks (this entire section will be recoded for update 1.1)
                            # ======================================================================================================================
                            if func.gettok(duckdata, 1, ',') == 'normal' or func.gettok(duckdata, 1, ',') == 'gold':
                                # determine if friend or unlucky
                                friendornot = random.randrange(1, 100, 1)
                                # friend
                                if friendornot <= friendrate:
                                    friend = int(friend) + 1
                                    bot.duckinfo(username, b'friend', str(friend))
                                    bot.data_check(username, 'lucky_charm')
                                    # does not have lucky charm
                                    if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)) == False:
                                        xp = int(xp) + duckexp
                                        bot.duckinfo(username, b'xp', str(xp))
                                        duck[duckid] = 'None'
                                        # confiscated guns returned silently after duck is befriended
                                        confiscatedguns = ''
                                        irc.send(
                                            b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314FRIEND\x03     The duck ate the piece of bread!     \x02\\_O< QUAAACK!\x02\x033   [BEFRIENDED DUCKS: ' + bytes(
                                                str(friend), 'utf-8') + b'] [+' + bytes(str(duckexp),
                                                                                        'utf-8') + b' xp]\x03\r\n')
                                        start_time = time.time()
                                        if duck_exists() == False:
                                            fear_factor = False
                                        # check for level up
                                        if int(xp) >= int(levelup):
                                            level_up(username)
                                        continue
                                    # has lucky charm
                                    if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)) == True:
                                        exp = duckexp * 2
                                        xp = int(xp) + exp
                                        bot.duckinfo(username, b'xp', str(xp))
                                        duck[duckid] = 'None'
                                        # confiscated guns returned silently after duck is befriended
                                        confiscatedguns = ''
                                        irc.send(
                                            b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314FRIEND\x03     The duck ate the piece of bread!     \x02\\_O< QUAAACK!\x02\x033   [BEFRIENDED DUCKS: ' + bytes(
                                                str(friend), 'utf-8') + b'] [+' + bytes(str(exp),
                                                                                        'utf-8') + b' xp - Lucky Charm]\x03\r\n')
                                        start_time = time.time()
                                        if duck_exists() == False:
                                            fear_factor = False
                                        # check for level up
                                        if int(xp) >= int(levelup):
                                            level_up(username)
                                        continue
                                # unlucky
                                if friendornot > friendrate:
                                    irc.send(
                                        b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034UNLUCKY\x03     The duck didn't seem to notice. Try again.     \x02\\_O< QUACK\x02\r\n")
                                    continue
                            # ======================================================================================================================
                            # !bef - golden ducks (this entire section will be recoded for update 1.1)
                            # ======================================================================================================================
                            if func.gettok(duckdata, 1, ',') == 'golden':
                                # determine if friend or unlucky (golden ducks are harder)
                                friendornot = random.randrange(0, 175, 1)
                                # friend
                                if friendornot <= friendrate:
                                    friend = int(friend) + 1
                                    bot.duckinfo(username, b'friend', str(friend))
                                    bot.data_check(username, 'lucky_charm')
                                    # does not have lucky charm
                                    if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)) == False:
                                        exp = duckexp * 3
                                        xp = int(xp) + exp
                                        bot.duckinfo(username, b'xp', str(xp))
                                        duck[duckid] = 'None'
                                        # confiscated guns returned silently after duck is befriended
                                        confiscatedguns = ''
                                        irc.send(
                                            b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314FRIEND\x03     The GOLDEN DUCK ate the piece of bread!     \x02\\_0< QUAAACK!\x02\x033   [BEFRIENDED DUCKS: ' + bytes(
                                                str(friend), 'utf-8') + b'] [+' + bytes(str(exp),
                                                                                        'utf-8') + b' xp]\x03\r\n')
                                        start_time = time.time()
                                        if duck_exists() == False:
                                            fear_factor = False
                                        # check for level up
                                        if int(xp) >= int(levelup):
                                            level_up(username)
                                        continue
                                    # has lucky charm
                                    if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)) == True:
                                        exp = duckexp * 3
                                        exp = exp * 2
                                        xp = int(xp) + exp
                                        bot.duckinfo(username, b'xp', str(xp))
                                        duck[duckid] = 'None'
                                        # confiscated guns returned silently after duck is befriended
                                        confiscatedguns = ''
                                        irc.send(
                                            b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314FRIEND\x03     The GOLDEN DUCK ate the piece of bread!     \x02\\_0< QUAAACK!\x02\x033   [BEFRIENDED DUCKS: ' + bytes(
                                                str(friend), 'utf-8') + b'] [+' + bytes(str(exp),
                                                                                        'utf-8') + b' xp - Lucky Charm]\x03\r\n')
                                        start_time = time.time()
                                        if duck_exists() == False:
                                            fear_factor = False
                                        # check for level up
                                        if int(xp) >= int(levelup):
                                            level_up(username)
                                        continue
                                # unlucky
                                if friendornot > friendrate:
                                    irc.send(
                                        b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034UNLUCKY\x03     The GOLDEN DUCK didn't seem to notice. Try again.     \x02\\_O< QUACK\x02\r\n")
                                    continue
                    # ======================================================================================================================
                    # !tshot - displays all the ducks shot
                    # ======================================================================================================================
                    if data[3].lower() == b':!tshot':
                        daily = func.cnfread('duckhunt.cnf', 'top_shot', 'daily')
                        weekly = func.cnfread('duckhunt.cnf', 'top_shot', 'weekly')
                        monthly = func.cnfread('duckhunt.cnf', 'top_shot', 'monthly')
                        totalshot = func.cnfread('duckhunt.cnf', 'top_shot', 'totalshot')
                        msg = '\x034Today:\x03\x037 ' + str(daily) + '\x03 \x034This Week:\x03\x037 ' + str(
                            weekly) + '\x03 \x034This Month:\x03\x037 ' + str(
                            monthly) + '\x03 \x034Since Last Reset:\x03\x037 ' + str(totalshot)
                        irc.send(
                            b'PRIVMSG ' + duckchan + b' :\x033[Super DuckHunt] Shot Ducks Statistics:\x03 ' + bytes(
                                str(msg), 'utf-8') + b'\x03\r\n')
                        continue
                    # ======================================================================================================================
                    # !dshot - displays the daily ducks shot
                    # ======================================================================================================================
                    if data[3].lower() == b':!dshot':
                        daily = func.cnfread('duckhunt.cnf', 'top_shot', 'daily')
                        irc.send(
                            b'PRIVMSG ' + duckchan + b' :\x033[Super DuckHunt] Daily Ducks Shot:\x03\x037 ' + bytes(
                                str(daily), 'utf-8') + b'\x03\r\n')
                        continue
                    # ======================================================================================================================
                    # !wshot - displays the weekly ducks shot
                    # ======================================================================================================================
                    if data[3].lower() == b':!wshot':
                        weekly = func.cnfread('duckhunt.cnf', 'top_shot', 'weekly')
                        irc.send(
                            b'PRIVMSG ' + duckchan + b' :\x033[Super DuckHunt] Weekly Ducks Shot:\x03\x037 ' + bytes(
                                str(weekly), 'utf-8') + b'\x03\r\n')
                        continue
                    # ======================================================================================================================
                    # !mshot - displays the monthly ducks shot
                    # ======================================================================================================================
                    if data[3].lower() == b':!mshot':
                        monthly = func.cnfread('duckhunt.cnf', 'top_shot', 'monthly')
                        irc.send(
                            b'PRIVMSG ' + duckchan + b' :\x033[Super DuckHunt] Monthly Ducks Shot:\x03\x037 ' + bytes(
                                str(monthly), 'utf-8') + b'\x03\r\n')
                        continue
                    # ======================================================================================================================
                    # !help
                    # ======================================================================================================================
                    if data[3].lower() == b':!help':
                        irc.send(
                            b'PRIVMSG ' + duckchan + b' :For DuckHunt HELP visit: https://neo-coder-usa.github.io/super-duckhunt-beta/\r\n')
                        continue
                    # ======================================================================================================================
                    # !spawnduck <normal/golden> - Botmaster and Admin only
                    # <normal/golden> is optional, if using just !spawnduck a normal duck is spawned.
                    # ======================================================================================================================
                    if data[3].lower() == b':!spawnduck':
                        dusername = username.decode()
                        if func.istok(botmaster, str(dusername), ',') == False and func.istok(adminlist, str(dusername),
                                                                                              ',') == False:
                            continue
                        if len(data) == 4:
                            for x in range(maxducks + 1):
                                if x == 0:
                                    continue
                                d_key = 'd' + str(x)
                                if duck[d_key] == 'None':
                                    spawnduck(d_key, 'normal')
                                    start_time = time.time()
                                    break
                                if x == maxducks:
                                    irc.send(
                                        b'NOTICE ' + username + b' :The maximum amount of ducks are currently spawned.\r\n')
                                    break
                                continue
                        if len(data) == 5:
                            if data[4].lower() == b'normal':
                                for x in range(maxducks + 1):
                                    if x == 0:
                                        continue
                                    d_key = 'd' + str(x)
                                    if duck[d_key] == 'None':
                                        spawnduck(d_key, 'normal')
                                        start_time = time.time()
                                        break
                                    if x == maxducks:
                                        irc.send(
                                            b'NOTICE ' + username + b' :The maximum amount of ducks are currently spawned.\r\n')
                                        break
                                    continue
                            if data[4].lower() == b'golden':
                                for x in range(maxducks + 1):
                                    if x == 0:
                                        continue
                                    d_key = 'd' + str(x)
                                    if duck[d_key] == 'None':
                                        spawnduck(d_key, 'gold')
                                        start_time = time.time()
                                        break
                                    if x == maxducks:
                                        irc.send(
                                            b'NOTICE ' + username + b' :The maximum amount of ducks are currently spawned.\r\n')
                                        break
                                    continue
                        continue
        # CONTINUE LOOP TO NEXT ITERATION ======================================================================================
        x += 1
        continue
# END OF MAIN LOOP # ===================================================================================================
