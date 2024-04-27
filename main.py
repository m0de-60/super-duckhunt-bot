#! /usr/bin/python3
# Mode60
# ABOUT INFO# ==========================================================================================================
# Title..........: Super DuckHunt v1.1.3-2 Python IRC Bot (BETA)
# File...........: main.py
# Python version.: v3.12.0 (does not work in older versions)
# Script version.: v1.1.3-2 BETA
# Remarks........: 1.1.3-2: Addition of a optional SSL connection. See operators manual for SSL configuration!
#                  1.1.3: Added relay bot capability and more fixes and adjustments from v1.1.2
# Language.......: English
# Description....: IRC Bot Script based off original DuckHunt bot by Menz Agitat
#                  Lots of changes and twists added to this, following suit as Menz Agitat bot was said to be a "port"
#                  of the NES game for IRC, This one would be equivelent to a SNES version, or a "sequel".
# Imports........: func.py, bot.py, configparser, threading, socket, time, random, math, datetime
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
# FUTURE THOUGHTS AND POSSIBILITIES ====================================================================================
# Get this version-series solid and off beta before going any further. 1.1.0+
# Add the laughing dog (optional feature, can be turned on/off)
# Add an accidental goose?
# Multi-channel?
# IMPORT # =============================================================================================================
from configparser import RawConfigParser
from datetime import date
import threading
import ssl
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
port = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'port'))  # use only port 6667 or 6697 for SSL
if func.cnfexists('duckhunt.cnf', 'duckhunt', 'serverssl') is False:
    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'serverssl', 'off')
serverssl = func.cnfread('duckhunt.cnf', 'duckhunt', 'serverssl')
duckchan = func.cnfread('duckhunt.cnf', 'duckhunt', 'duckchan').encode()
duckchan = duckchan.lower()
botname = func.cnfread('duckhunt.cnf', 'duckhunt', 'botname').encode()
botpass = str(func.cnfread('duckhunt.cnf', 'duckhunt', 'botpass'))
botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster').lower()
adminlist = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin').lower()
botignore = func.cnfread('duckhunt.cnf', 'duckhunt', 'ignore').lower()
spawntime = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'spawntime'))
flytime = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'flytime'))
maxducks = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'maxducks'))
duckexp = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'duckexp'))
duckfear = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'duckfear'))
duckgold = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'duckgold'))
friendrate = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'friendrate'))
# update 1.1.0 MAINTENANCE VALUES ======================================================================================
maint = int(func.cnfread('duckhunt.cnf', 'duckhunt', 'maint'))
maint_time = func.cnfread('duckhunt.cnf', 'duckhunt', 'maint_time')
if str(maint_time) == '0' and maint > 0:
    maint_time = str(time.time())
    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'maint_time', str(time.time()))
# update 1.1.0 CONFIGURATION 'RULES' VARIABLES =========================================================================
thebushes = int(func.cnfread('duckhunt.cnf', 'rules', 'thebushes'))
gunconf = func.cnfread('duckhunt.cnf', 'rules', 'gunconf')
infammo = func.cnfread('duckhunt.cnf', 'rules', 'infammo')
gunricochet = int(func.cnfread('duckhunt.cnf', 'rules', 'gunricochet'))
bang = func.cnfread('duckhunt.cnf', 'rules', 'bang')
bef = func.cnfread('duckhunt.cnf', 'rules', 'bef')
# FLOOD CHECK VALUES # =================================================================================================
flood_check = False
if func.cnfread('duckhunt.cnf', 'duckhunt', 'floodcheck') != '0':
    flood_check = True
# ADD-ON FOR RELAY BOTS (WORKING SORT OF) v1.1.3 ===================================================================
if func.cnfexists('duckhunt.cnf', 'duckhunt', 'relays') is False:
    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'relays', '0')
relaybot = func.cnfread('duckhunt.cnf', 'duckhunt', 'relays').lower()
# GLOBAL VARIABLES # ===================================================================================================
botversion = b'1.1.3-2'  # Current Bot Version hard code DO NOT CHANGE
# =========================================================
duckhunt = True  # Main duckhunt control
# =========================================================
irc = ''
userlist = {}  # For channel user monitoring
userchan = 0  # For channel user monitoring
duckexists = False  # does a duck exist? always leave this as false
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
keep_alive = ''  # For SSL stuff, v1.1.3-2
daily = func.cnfread('duckhunt.cnf', 'top_shot', 'daily')  # daily shots
weekly = func.cnfread('duckhunt.cnf', 'top_shot', 'weekly')  # weekly shots
monthly = func.cnfread('duckhunt.cnf', 'top_shot', 'monthly')  # monthly shots
totalshot = func.cnfread('duckhunt.cnf', 'top_shot', 'totalshot')  # total shots
month = func.cnfread('duckhunt.cnf', 'top_shot', 't_month')
week = func.cnfread('duckhunt.cnf', 'top_shot', 't_week')
day = func.cnfread('duckhunt.cnf', 'top_shot', 't_day')

# topduck fix #1 of many - update 1.1.0
if not func.cnfexists('duckhunt.cnf', 'ducks', 'cache'):
    func.cnfwrite('duckhunt.cnf', 'ducks', 'cache', '0')

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
# Syntax.........: duckstats(user, ruser) (use duckstats(user, ruser, 'opt') for relay bots for PRIVMSG)
# Parameters.....: user - username to send data to
#                  ruser - username of stats to be displayed
# Return values..: Returns 1 after sending stats to user.
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
# noinspection PyUnboundLocalVariable,PySimplifyBooleanCheck,PyShadowingNames
def duckstats(user, ruser, ext=''):
    # No stats/user hasn't played
    if func.cnfexists('duckhunt.cnf', 'ducks', str(ruser)) is False and isconnect is True:
        if ext != '':
            irc.send(b'PRIVMSG ' + duckchan + b' :' + ruser + b' > Has not played yet.\r\n')
            return 0
        irc.send(b'NOTICE ' + user + b' :' + ruser + b' > Has not played yet.\r\n')
        return 0
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
    if float(reliability) <= 65:
        gunstatus = b'Needs cleaning'
    elif func.istok(jammedguns, str(username), ',') is True:
        gunstatus = b'Jammed'
    elif func.istok(confiscatedguns, str(username), ',') is True and gunconf == 'on':
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
    loaf = func.gettok(bot.duckinfo(ruser, b'bread'), 2, '?').encode()
    mloaf = func.gettok(bot.duckinfo(ruser, b'bread'), 3, '?').encode()
    friend = bot.duckinfo(ruser, b'friend').encode()

    if infammo == 'on':
        scorebox = b'\x030,1[SCORE]\x037,1 Best Time:\x034,1 ' + besttime + b' \x030,1|\x037,1 Level:\x034,1 ' + level + b' \x030,1|\x037,1 xp:\x034,1 ' + xp + b' \x030,1|\x037,1 Ducks:\x034,1 ' + ducks + b' \x030,1|\x037,1 Golden Ducks:\x034,1 ' + gducks + b' \x030,1|\x037,1 Befriended Ducks:\x034,1 ' + friend + b' \x030,1|\x037,1 Accidents:\x034,1 ' + accidents
        breadbox = b'\x030,1[BREAD BOX]\x037,1 Bread Pieces:\x034,1 ' + bread + b'/' + mbread + b' \x030,1|\x037,1 Loaf: \x02\x033Inf\x02'
        gunbox = b'\x030,1[GUN STATS]\x037,1 Status:\x034,1 ' + gunstatus + b' \x030,1|\x037,1 Rounds:\x034,1 ' + rounds + b'/' + mrounds + b' \x030,1|\x037,1 Magazines: \x02\x033Inf\x02\x03 \x030,1|\x037,1 Accuracy:\x034,1 ' + accuracy + b'% \x030,1|\x037,1 Current Reliability:\x034,1 ' + reliability + b'% \x030,1|\x037,1 Max Reliability:\x034,1 ' + mreliability + b'%'

    if infammo == 'off':
        scorebox = b'\x038,1[SCORE]\x037,1 Best Time:\x034,1 ' + besttime + b' \x030,1|\x037,1 Level:\x034,1 ' + level + b' \x030,1|\x037,1 xp:\x034,1 ' + xp + b' \x030,1|\x037,1 Ducks:\x034,1 ' + ducks + b' \x030,1|\x037,1 Golden Ducks:\x034,1 ' + gducks + b' \x030,1|\x037,1 Befriended Ducks:\x034,1 ' + friend + b' \x030,1|\x037,1 Accidents:\x034,1 ' + accidents
        breadbox = b'\x038,1[BREAD BOX]\x037,1 Bread Pieces:\x034,1 ' + bread + b'/' + mbread + b' \x030,1|\x037,1 Loaf:\x034,1 ' + loaf + b'/' + mloaf
        gunbox = b'\x038,1[GUN STATS]\x037,1 Status:\x034,1 ' + gunstatus + b' \x030,1|\x037,1 Rounds:\x034,1 ' + rounds + b'/' + mrounds + b' \x030,1|\x037,1 Magazines:\x034,1 ' + mags + b'/' + mmags + b' \x030,1|\x037,1 Accuracy:\x034,1 ' + accuracy + b'% \x030,1|\x037,1 Current Reliability:\x034,1 ' + reliability + b'% \x030,1|\x037,1 Max Reliability:\x034,1 ' + mreliability + b'%'

    hbe = bot.inveffect(str(ruser))
    huntingbag = func.gettok(hbe, 0, '::')
    huntingbag = huntingbag.encode()
    effectsbox = func.gettok(hbe, 1, '::')
    effectsbox = effectsbox.encode()
    if isconnect is True:
        if ext != '':
            irc.send(b'PRIVMSG ' + duckchan + b' :\x038,1[DuckStats:\x037,1 ' + ruser + b'\x038,1] ' + scorebox + b' ' + gunbox + b'\r\n')
            irc.send(b'PRIVMSG ' + duckchan + b' :' + breadbox + b' ' + effectsbox + b'\r\n')
            irc.send(b'PRIVMSG ' + duckchan + b' :' + huntingbag + b'\r\n')
            return 2
        irc.send(b'NOTICE ' + user + b' :\x038,1[DuckStats:\x037,1 ' + ruser + b'\x038,1] ' + scorebox + b' ' + gunbox + b'\r\n')
        irc.send(b'NOTICE ' + user + b' :' + breadbox + b' ' + effectsbox + b'\r\n')
        irc.send(b'NOTICE ' + user + b' :' + huntingbag + b'\r\n')
        return 1
    return 0
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
    if exitvar != 'Disconnect' and exitvar != 'Disconnect2':

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
        # v1.1.3-2 for SSL Eof handling
        global keep_alive
        keep_alive = time.time()
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
        # added 'Disconnect2' for SSL stuff v1.1.32
        if exitvar == 'Disconnect2':
            break

        # duck spawn/flee timer handling =======================================================================================
        if not duckhunt:
            continue
        time.sleep(10)  # fastest this way ¯\_(o.O)_/¯
        if serverssl == 'on':  # v 1.1.3-2 SSL stuff
            keepalive()
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

# v.1.1.3-2 keep alive function (derived from pycore)
def keepalive():
    global keep_alive
    time_result = round(time.time() - float(keep_alive))
    if time_result >= 90:
        print('SSL Keep Alive --> PING :PYDUCKQUACK')
        irc.send(b'PING :PYDUCKQUACK\r\n')
        keep_alive = time.time()

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
    names = names.lower()
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
# Remarks........: Update 1.1.0 - recoded, changed prizes and altered levelup values
# ======================================================================================================================
# noinspection PyShadowingNames
def level_up(user):
    # increase level by 1
    level = bot.duckinfo(user, b'level')
    level = int(level) + 1
    bot.duckinfo(user, b'level', str(level))

    # increase level up
    xp = bot.duckinfo(user, b'xp')
    levelup = int(xp) + 800
    if int(xp) > 10000:
        levelup = int(xp) + 2400
    if int(xp) < 10000 and int(xp) > 5000:
        levelup = int(xp) + 1600
    bot.duckinfo(user, b'levelup', str(levelup))

    global bang
    bang = func.cnfread('duckhunt.cnf', 'rules', 'bang')
    # determine prize
    drawprize = random.randint(1, 4)
    prize = ''
    prizedesc = ''

    # prize 1 full ammo (or full bread)
    if drawprize == 1:
        if bang == 'on':
            prize = 'Ammo Fill-up'
            prizedesc = 'Ammo has been filled.'

            # fill ammo
            ammo = bot.duckinfo(user, b'ammo')
            mrounds = func.gettok(ammo, 2, '?')
            rounds = mrounds
            mmags = func.gettok(ammo, 3, '?')
            mags = mmags
            ammo = rounds + '?' + mags + '?' + mrounds + '?' + mmags
            bot.duckinfo(user, b'ammo', str(ammo))

        if bang == 'off':
            prize = 'Bread Fill-up'
            prizedesc = 'Bread has been filled.'

            # fill bread
            breadbox = bot.duckinfo(user, b'bread')
            mbread = func.gettok(breadbox, 1, '?')
            mloaf = func.gettok(breadbox, 3, '?')
            bread = mbread
            loaf = mloaf
            breadbox = bread + '?' + mbread + '?' + loaf + '?' + mloaf
            bot.duckinfo(user, b'bread', str(breadbox))

    # prize 2 rain coat
    if drawprize == 2:
        prize = 'Rain Coat'
        prizedesc = 'This will prevent getting soggy and sheild against a duck bomb for 24 hours.'
        func.cnfwrite('duckhunt.cnf', 'rain_coat', str(user), str(time.time()))

    # prize 3 sunglasses
    if drawprize == 3:
        prize = 'Sunglasses'
        prizedesc = 'You are protected from bedazzlement for 24 hours.'
        func.cnfwrite('duckhunt.cnf', 'sunglasses', str(user), str(time.time()))

    # prize 4 bread or duck booklet
    if drawprize == 4:
        if bang == 'on':
            prize = 'Bread Fill-up'
            prizedesc = 'Bread has been filled.'

            # fill bread
            breadbox = bot.duckinfo(user, b'bread')
            mbread = func.gettok(breadbox, 1, '?')
            mloaf = func.gettok(breadbox, 3, '?')
            bread = mbread
            loaf = mloaf
            breadbox = bread + '?' + mbread + '?' + loaf + '?' + mloaf
            bot.duckinfo(user, b'bread', str(breadbox))

        if bang == 'off':
            prize = 'Duck Booklet'
            prizedesc = 'The booklet earns an extra 45 xp!'

            xp = bot.duckinfo(user, b'xp')
            xp = int(xp) + 45
            bot.duckinfo(user, b'xp', str(xp))

    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Has leveled up! ' + username + b' has reached level ' + bytes(str(level), 'utf-8') + b'! Prize won: ' + bytes(str(prize), 'utf-8') + b'. ' + bytes(str(prizedesc), 'utf-8') + b'\r\n')
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
    # namech = name.replace("b'", '')
    # namech = namech.replace("'", '')
    namech = name.lower()
    # print('userchan ' + str(userchan))
    nnx = 1
    while nnx <= userchan:
        nd_key = 'cl' + str(nnx)
        print('NAMES: ' + str(userlist[nd_key]))
        if func.istok(userlist[nd_key], namech, ' '):
            return True
        if func.istok(userlist[nd_key], namech + ']', ' '):
            return True
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
def shopmenu(user, opt=''):
    # ammo = bot.duckinfo(user, b'ammo')
    # rounds = func.gettok(ammo, 0, '?')
    # mags = func.gettok(ammo, 1, '?')
    # mrounds = func.gettok(ammo, 2, '?')
    # mmags = func.gettok(ammo, 3, '?')

    # single bullet
    shop1 = '1:\x037,1 Single Round\x034,1 (' + str(bot.shopprice(user, 1)) + ' xp)'
    if infammo == 'on':
        shop1 = '1:\x0314,1 Single Round (' + str(bot.shopprice(user, 1)) + ' xp)'
    # refill magazine
    shop2 = '2:\x037,1 Refill Magazine\x034,1 (' + str(bot.shopprice(user, 2)) + ' xp)'
    if infammo == 'on':
        shop2 = '2:\x0314,1 Refill Magazine (' + str(bot.shopprice(user, 1)) + ' xp)'
    # gun cleaning
    shop3 = '3:\x037,1 Gun Cleaning\x034,1 (' + str(bot.shopprice(user, 3)) + ' xp)'
    # explosive ammo
    shop4 = '4:\x037,1 Explosive Ammo\x034,1 (' + str(bot.shopprice(user, 4)) + ' xp)'
    # return confiscated gun
    shop5 = '5:\x037,1 Return Confiscated Gun\x034,1 (' + str(bot.shopprice(user, 5)) + ' xp)'
    if gunconf == 'off':
        shop5 = '5:\x0314,1 Return Confiscated Gun (' + str(bot.shopprice(user, 5)) + ' xp)'
    # gun grease
    shop6 = '6:\x037,1 Gun Grease\x034,1 (' + str(bot.shopprice(user, 6)) + ' xp)'
    # gun upgrade
    shop7 = '7:\x037,1 Gun Upgrade\x034,1 (' + str(bot.shopprice(user, 7)) + ' xp)'
    # Gun Lock
    shop8 = '8:\x037,1 Gun Lock\x034,1 (' + str(bot.shopprice(user, 8)) + ' xp)'
    # silencer
    shop9 = '9:\x037,1 Silencer\x034,1 (' + str(bot.shopprice(user, 9)) + ' xp)'
    # lucky charm
    shop10 = '10:\x037,1 Lucky Charm\x034,1 (' + str(bot.shopprice(user, 10)) + ' xp)'
    # sunglasses
    shop11 = '11:\x037,1 Sunglasses\x034,1 (' + str(bot.shopprice(user, 11)) + ' xp)'
    # new clothes
    shop12 = '12:\x037,1 New Clothes\x034,1 (' + str(bot.shopprice(user, 12)) + ' xp)'
    # eye drops
    shop13 = '13:\x037,1 Eye Drops\x034,1 (' + str(bot.shopprice(user, 13)) + ' xp)'
    # mirror
    shop14 = '14:\x037,1 Mirror\x034,1 (' + str(bot.shopprice(user, 14)) + ' xp)'
    # handful of sand
    shop15 = '15:\x037,1 Handful of Sand\x034,1 (' + str(bot.shopprice(user, 15)) + ' xp)'
    # water bucket
    shop16 = '16:\x037,1 Water Bucket\x034,1 (' + str(bot.shopprice(user, 16)) + ' xp)'
    # sabotage
    shop17 = '17:\x037,1 Sabotage\x034,1 (' + str(bot.shopprice(user, 17)) + ' xp)'
    # accident insurance
    shop18 = '18:\x037,1 Accident Insurance\x034,1 (' + str(bot.shopprice(user, 18)) + ' xp)'
    if gunconf == 'off':
        shop18 = '18:\x0314,1 Accident Insurance (' + str(bot.shopprice(user, 18)) + ' xp)'
    # loaf of bread
    shop19 = '19:\x037,1 Loaf of Bread\x034,1 (' + str(bot.shopprice(user, 19)) + ' xp)'
    if infammo == 'on':
        shop19 = '19:\x0314,1 Loaf of Bread (' + str(bot.shopprice(user, 19)) + ' xp)'
    # bag of popcorn
    shop20 = '20:\x037,1 Bag of Popcorn\x034,1 (' + str(bot.shopprice(user, 20)) + ' xp)'
    # bread box lock
    shop21 = '21:\x037,1 Bread Box Lock\x034,1 (' + str(bot.shopprice(user, 21)) + ' xp)'
    # rain coat
    shop22 = '22:\x037,1 Rain Coat\x034,1 (' + str(bot.shopprice(user, 22)) + ' xp)'
    # magazine upgrade
    shop23 = '23:\x037,1 Magazine Upgrade\x034,1 (' + str(bot.shopprice(user, 23)) + ' xp)'
    # additional magazine
    shop24 = '24:\x037,1 Additional Magazine\x034,1 (' + str(bot.shopprice(user, 24)) + ' xp)'
    if infammo == 'on':
        shop24 = '24:\x0314,1 Additional Magazine (' + str(bot.shopprice(user, 24)) + ' xp)'

    # prepares menus
    # !bang off !bef on menu
    if bang == 'off' and bef == 'on':
        menu1 = '\x038,1[Shop Menu]\x034,1 ' + shop10 + ' \x037,1|\x034,1 ' + shop11 + ' \x037,1|\x034,1 ' + shop12 + ' \x037,1|\x034,1 ' + shop13 + ' \x037,1|\x034,1 ' + shop14
        menu2 = '\x038,1[Shop Menu]\x034,1 ' + shop16 + ' \x037,1|\x034,1 ' + shop19 + ' \x037,1|\x034,1 ' + shop20 + ' \x037,1|\x034,1 ' + shop21 + ' \x037,1|\x034,1 ' + shop22
        if opt != '':
            irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu1), 'utf-8') + b'\r\n')
            irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu2), 'utf-8') + b'\r\n')
            irc.send(b'PRIVMSG ' + duckchan + b' :\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]\r\n')
            return
        irc.send(b'NOTICE ' + username + b' :' + bytes(str(menu1), 'utf-8') + b'\r\n')
        irc.send(b'NOTICE ' + username + b' :' + bytes(str(menu2), 'utf-8') + b'\r\n')
        irc.send(b'NOTICE ' + username + b' :\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]\r\n')
        return

    # !bang on !bef off menu
    elif bang == 'on' and bef == 'off':
        menu1 = '\x038,1[Shop Menu]\x034,1 ' + shop1 + ' \x037,1|\x034,1 ' + shop2 + ' \x037,1|\x034,1 ' + shop3 + ' \x037,1|\x034,1 ' + shop4 + ' \x037,1|\x034,1 ' + shop5 + ' \x037,1|\x034,1 ' + shop6 + ' \x037,1|\x034,1 ' + shop7 + ' \x037,1|\x034,1 ' + shop8 + ' \x037,1|\x034,1 ' + shop9 + ' \x037,1|\x034,1 ' + shop10
        menu2 = '\x038,1[Shop Menu]\x034,1 ' + shop11 + ' \x037,1|\x034,1 ' + shop12 + ' \x037,1|\x034,1 ' + shop13 + ' \x037,1|\x034,1 ' + shop14 + ' \x037,1|\x034,1 ' + shop15 + ' \x037,1|\x034,1 ' + shop16 + ' \x037,1|\x034,1 ' + shop17 + ' \x037,1|\x034,1 ' + shop18 + ' \x037,1|\x034,1 ' + shop22
        menu3 = '\x038,1[Shop Menu]\x034,1 ' + shop23 + ' \x037,1|\x034,1 ' + shop24
        if opt != '':
            irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu1), 'utf-8') + b'\r\n')
            irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu2), 'utf-8') + b'\r\n')
            irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu3), 'utf-8') + b'\r\n')
            irc.send(b'PRIVMSG ' + duckchan + b' :\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]\r\n')
            return
        irc.send(b'NOTICE ' + username + b' :' + bytes(str(menu1), 'utf-8') + b'\r\n')
        irc.send(b'NOTICE ' + username + b' :' + bytes(str(menu2), 'utf-8') + b'\r\n')
        irc.send(b'NOTICE ' + username + b' :' + bytes(str(menu3), 'utf-8') + b'\r\n')
        irc.send(b'NOTICE ' + username + b' :\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]\r\n')
        return

    # normal menu (!bang on, !bef on,
    elif bang == 'on' and bef == 'on':
        menu1 = '\x038,1[Shop Menu]\x034,1 ' + shop1 + ' \x037,1|\x034,1 ' + shop2 + ' \x037,1|\x034,1 ' + shop3 + ' \x037,1|\x034,1 ' + shop4 + ' \x037,1|\x034,1 ' + shop5 + ' \x037,1|\x034,1 ' + shop6 + ' \x037,1|\x034,1 ' + shop7 + ' \x037,1|\x034,1 ' + shop8 + ' \x037,1|\x034,1 ' + shop9 + ' \x037,1|\x034,1 ' + shop10
        menu2 = '\x038,1[Shop Menu]\x034,1 ' + shop11 + ' \x037,1|\x034,1 ' + shop12 + ' \x037,1|\x034,1 ' + shop13 + ' \x037,1|\x034,1 ' + shop14 + ' \x037,1|\x034,1 ' + shop15 + ' \x037,1|\x034,1 ' + shop16 + ' \x037,1|\x034,1 ' + shop17 + ' \x037,1|\x034,1 ' + shop18 + ' \x037,1|\x034,1 ' + shop19 + ' \x037,1|\x034,1 ' + shop20
        menu3 = '\x038,1[Shop Menu]\x034,1 ' + shop21 + ' \x037,1|\x034,1 ' + shop22 + ' \x037,1|\x034,1 ' + shop23 + ' \x037,1|\x034,1 ' + shop24
        if opt != '':
            irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu1), 'utf-8') + b'\r\n')
            irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu2), 'utf-8') + b'\r\n')
            irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu3), 'utf-8') + b'\r\n')
            irc.send(b'PRIVMSG ' + duckchan + b' :\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]\r\n')
            return
        irc.send(b'NOTICE ' + username + b' :' + bytes(str(menu1), 'utf-8') + b'\r\n')
        irc.send(b'NOTICE ' + username + b' :' + bytes(str(menu2), 'utf-8') + b'\r\n')
        irc.send(b'NOTICE ' + username + b' :' + bytes(str(menu3), 'utf-8') + b'\r\n')
        irc.send(b'NOTICE ' + username + b' :\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]\r\n')
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
            irc.send(b'PRIVMSG ' + duckchan + b" :\x0314-.,\xc2\xb8\xc2\xb8.-\xc2\xb7\xc2\xb0'`'\xc2\xb0\xc2\xb7-.,\xc2\xb8\xc2\xb8.-\xc2\xb7\xc2\xb0'`'\xc2\xb0\xc2\xb7\x0f \x02\\_O<\x02   \x0314QUACK\x0f\r\n")
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
        # print(datkey)
        dat = func.cnfread('duckhunt.cnf', 'ducks', datkey)
        # print(dat)
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
    # print('GATHER: ' + str(datt))

    # Determine if only 1 top duck or multiple, if more than one, continues if not, sends message.
    if func.numtok(datt, ',') == 1:
        # print('only one top duck')
        usr = func.gettok(datt, 0, ',')
        # print('USER: ' + str(usr))
        if isconnect:
            irc.send(b'PRIVMSG ' + duckchan + b' :The top duck is: ' + func.gettok(usr, 1, "'").encode() + b' ' + func.gettok(datt, 0, '?').encode() + b' xp\r\n')
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
    # print('TOP DUCKS: ' + str(topdmsg))
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
        bot.debug('0', 'The total shots for the day has been automatically reset for a new day.')
        day = current_day
        func.cnfwrite('duckhunt.cnf', 'top_shot', 't_day', str(day))
        if isconnect is True and duckhunt is True:
            irc.send(b'PRIVMSG ' + duckchan + b' :Total ducks shot for yesterday: ' + bytes(str(daily), 'utf-8') + b' The daily total shots has been reset for a new day!\r\n')
        daily = 0
        func.cnfwrite('duckhunt.cnf', 'top_shot', 'daily', str(daily))
    if str(current_week) != str(week):
        bot.debug('0', 'The total shots for the week has been automatically reset for a new week.')
        week = current_week
        func.cnfwrite('duckhunt.cnf', 'top_shot', 't_week', str(week))
        if isconnect is True and duckhunt is True:
            irc.send(b'PRIVMSG ' + duckchan + b' :Total ducks shot for last week: ' + bytes(str(weekly), 'utf-8') + b' The weekly total shots has been reset for a new week!\r\n')
        weekly = 0
        func.cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', str(weekly))
    if str(current_month) != str(month):
        month = current_month
        func.cnfwrite('duckhunt.cnf', 'top_shot', 't_month', str(month))
        if isconnect is True and duckhunt is True:
            irc.send(b'PRIVMSG ' + duckchan + b' :Total ducks shot for last month: ' + bytes(str(monthly), 'utf-8') + b' The monthly total shots has been reset for a new month!\r\n')
        monthly = 0
        func.cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', str(monthly))
    return
# ===> top_shot

# for UTF error fix v1.1.3
def utfix(datatext):
    try:
        datatext.decode()
        # print('UTFIX: True')
        return True
    except UnicodeError:
        # print('UTFIX: False')
        return False

# for SSL error handling (EOF errors??) band-aid pt 1.
# Forces bot to disconnect and reconnect. v.1.132
def ssl_err(args):
    global exitvar
    # irc.send(b'QUIT :Restarting...\r\n')
    exitvar = 'Disconnect2'
    # irc.close()
    # irc.send(b'QUIT :SSL connection error has forced the bot to restart...\r\n')
    print(f'*** SSL Error: {args.exc_value}')
    print(f'*** RESTARTING....')

    return

# for SSL error handling (EOF errors??) band-aid pt 2. (Crash prevent?)
# After ssl_err(args) is complete, this begins the reconnection process.
def err_reconnect():
    global irc
    global exitvar
    exitvar = 'Connect'
    irc.close()
    time.sleep(3)
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))
    if serverssl == 'on':
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.verify_opt = ssl.OP_NO_TLSv1_3
        irc = context.wrap_socket(irc, server_hostname=server)
    irc.send(b"USER " + botname + b" " + botname + b" " + botname + b" :Super DuckHunt Python Version by Neo_Nemesis\r\n")
    irc.send(b"NICK " + botname + b"\r\n")
    if str(botpass) != '0':
        irc.send(b'PASS ' + bytes(str(botpass), 'utf-8') + b'\r\n')


# ======================================================================================================================
# MAIN LOOP STUFF
# ======================================================================================================================

# ======================================================================================================================
# Connect to server
# ======================================================================================================================
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
if serverssl == 'on':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    irc = context.wrap_socket(irc, server_hostname=server)
irc.send(b"USER " + botname + b" " + botname + b" " + botname + b" :Super DuckHunt Python Version by Neo_Nemesis\r\n")
irc.send(b"NICK " + botname + b"\r\n")
if str(botpass) != '0':
    irc.send(b'PASS ' + bytes(str(botpass), 'utf-8') + b'\r\n')
# ======================================================================================================================
# main loop - start
# ======================================================================================================================
while 1:
    # if bot gets disocnnect, will attempt to reconnect.
    # Added 'Disconnect2' for adding SSL v1.1.32
    if exitvar == 'Disconnect' or exitvar == 'Disconnect2':
        if exitvar == 'Disconnect2':
            err_reconnect()
            continue
        time.sleep(5)
        exitvar = 'Connect'
        irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc.connect((server, port))
        if serverssl == 'on':
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.verify_opt = ssl.OP_NO_TLSv1_3
            irc = context.wrap_socket(irc, server_hostname=server)
        irc.send(b"USER " + botname + b" " + botname + b" " + botname + b" :Super DuckHunt Python Version by Neo_Nemesis\r\n")
        irc.send(b"NICK " + botname + b"\r\n")
        if botpass != '0':
            irc.send(b'PASS ' + bytes(str(botpass), 'utf-8') + b'\r\n')
        continue
    # total shots timer
    if isconnect and duckhunt is True:
        # determine bot maintenance
        if func.cnfread('duckhunt.cnf', 'duckhunt', 'maint') != '0':
            maint_time = func.cnfread('duckhunt.cnf', 'duckhunt', 'maint_time')
            cmtime = time.time() - float(maint_time)
            if float(cmtime) >= float(func.hourtosec(maint)):
                if duckhunt == True:
                    duckhunt = False
                irc.send(b'PRIVMSG ' + duckchan + b' :DuckHunt is temporarily off-line for routine scheduled bot maintenance. Please wait, this will only take a moment...\r\n')
                bot.cnfcleanup()
                func.cnfwrite('duckhunt.cnf', 'duckhunt', 'maint_time', str(time.time()))
                if duckhunt == False:
                    duckhunt = True
                irc.send(b'PRIVMSG ' + duckchan + b' :Bot maintenance complete. DuckHunt is back on-line!\r\n')
                continue
        top_shot()
    # IRC stuff
    text = irc.recv(2040)
    txt = text.splitlines()
    x = 0
    for x in range(len(txt)):
        # v 1.1.2 changed here to remove bytes decoding.
        print(b'DATA RECV: ' + txt[x])
        data = txt[x].split(b" ")
        # Server ping
        if data[0] == b'PING':
            keep_alive = time.time()
            irc.send(b"PONG " + data[1] + b'\r\n')
            continue
        if len(data) > 1 and data[1] == b'PONG':
            print('SSL Keep Alive - Ping/Pong LAG: ' + str(round(time.time() - keep_alive, 2)) + ' seconds')
            continue
        # Excess flood reconnect v 1.1.2
        if data[0].lower() == b'error':
            if data[1].lower() == b':closing' and data[2].lower() == b'link:':
                if flood_cont is True:
                    flood_cont = False
                exitvar = 'Disconnect'
                time.sleep(3)
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
                threading.excepthook = ssl_err
                timer_thread = threading.Thread(target=duck_timer)
                timer_thread.start()
# ======================================================================================================================
# /NAMES list - for user list control
# ======================================================================================================================
            if data[1] == b'353' and duckhunt is True and flood_cont is False:
                ircnamesrf(str(data))  # update v 1.1.0 flood protection
# ======================================================================================================================
# Events handling (Join, mode, part/quit, kick, nick
# Also calls /NAMES whenever user info changes on the channel
# update v 1.1.0 added stuff for flood protection
# ======================================================================================================================
            # join events
            if data[1] == b'JOIN' and flood_cont is False and duckhunt == True:
                temp = txt[x].split(b'!')
                username = temp[0].strip(b':')
                if str(username) != str(botname.lower()):
                    ircnamesrf('0', 'r')
                    irc.send(b'NAMES ' + duckchan + b'\r\n')
                continue
            # mode events
            if data[1] == b'MODE' and flood_cont is False and duckhunt == True:
                if data[2].lower() == duckchan:
                    ircnamesrf('0', 'r')
                    irc.send(b'NAMES ' + duckchan + b'\r\n')
                continue
            # part/quit events
            if data[1] == b'PART' or data[1] == b'QUIT':
                if flood_cont != False:
                    continue
                temp = txt[x].split(b'!')
                username = temp[0].strip(b':')
                # if bot disconnects, reconnects automatically after 5 seconds
                if str(username) == str(botname.lower()) and data[1] == b'QUIT':
                    exitvar = 'Disconnect'
                    isconnect = False
                    continue
                # flood control
                if flood_cont is True or duckhunt is False:
                    continue
                # userlist update
                if str(username) != str(botname.lower()) and data[2].lower() == duckchan:
                    ircnamesrf('0', 'r')
                    irc.send(b'NAMES ' + duckchan + b'\r\n')
                continue
            # kick events
            if data[1] == b'KICK':
                # rejoin channel when kicked
                if data[2].lower() == duckchan and data[3].lower() == botname.lower():
                    irc.send(b'JOIN ' + duckchan + b'\r\n')
                    continue
                # flood control
                if duckhunt == False:
                    continue
                # user list update
                if flood_cont == False:
                    ircnamesrf('0', 'r')
                    irc.send(b'NAMES ' + duckchan + b'\r\n')
                continue
            # nick events
            if data[1] == b'NICK' and flood_cont == False and duckhunt == True:
                if data[2].lower() == duckchan:
                    ircnamesrf('0', 'r')
                    irc.send(b'NAMES ' + duckchan + b'\r\n')
                    continue
                continue
# ======================================================================================================================
# PRIVMSG stuff (Channel & PM)
# ======================================================================================================================
            if data[1] == b'PRIVMSG':
                # relay bot stuff v1.1.3
                data3 = b''  # command (data[5])
                data4 = b''  # itemid (data[6])
                data5 = b''  # target/username (data[7])
                datarelay = False
                # Parse requesting username, and check for ignore
                temp = txt[x].split(b'!')
                username = temp[0].strip(b':')
                dusername = username.decode()  # for botmaster, admin, ignore, and to fix case sensative bug v1.1.0
                dusername = dusername.lower()
                # check is user is a relay v1.1.3
                if func.istok(relaybot, dusername, ',') is True and len(data) < 6:
                    continue
                if func.istok(relaybot, dusername, ',') is True and len(data) >= 6:
                    rbusername = data[4].decode()
                    # rbusername = rbusername.lower()
                    rbusername = func.striptext(rbusername)
                    rbusername = rbusername.replace('<', '')
                    rbusername = rbusername.replace('>', '')
                    rbusername = rbusername.replace('', '')
                    rbusername = rbusername.replace('', '')
                    print('rbusername: ' + func.striptext(rbusername))
                    # username = rbusername.encode()
                    rbusername = bytes(str(rbusername), 'utf-8')
                    username = rbusername
                    dusername = username.decode()
                    dusername = dusername.lower()
                    if func.cnfexists('duckhunt.cnf', 'ducks', str(username)) == True:
                        if bot.duckinfo(username, b'inv') != '1':
                            bot.duckinfo(username, b'inv', '1')
                    data3 = data[5].lower()
                    if len(data) > 6:
                        data4 = data[6]
                    if len(data) > 7:
                        data5 = data[7]
                    # print('rbusername data: ' + func.striptext(rbusername) + ' ' + str(data3) + ' ' + str(data4) + ' ' + str(data5))
                    datarelay = True
                # if user is not relay v1.1.3
                # rebot = bot.duckinfo(username, b'inv')
                # if datarelay == False and rebot != '0':
                #    bot.duckinfo(username, b'inv', '0')
                if datarelay == False and func.cnfexists('duckhunt.cnf', 'ducks', str(username)) == True:
                    if bot.duckinfo(username, b'inv') == '1':
                        bot.duckinfo(username, b'inv', '0')
                if func.istok(botignore, dusername, ',') is True:
                    continue
                if duckhunt is False and func.istok(botmaster, dusername, ',') is False and func.istok(adminlist, dusername, ',') is False:
                    time.sleep(2)
                    continue

# ======================================================================================================================
# Flood control here
# ======================================================================================================================
                # flood control activated
                if flood_check is True and flood_cont is True and duckhunt is True:
                    if data[3] == b':!flood' or data3 == b'!flood':
                        # temp = txt[x].split(b'!')
                        # username = temp[0].strip(b':')
                        adminlist = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin').lower()
                        botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster').lower()
                        if func.istok(adminlist, dusername, ',') is True or func.istok(botmaster, dusername, ',') is True:
                            flood_time = time.time()
                            flood = 0
                            flood_cont = False
                            irc.send(b'PRIVMSG ' + duckchan + b' :\x037* Flood Control Overide by ' + username + b' *\x03\r\n')
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
                elif flood_check is True and flood_cont is False and duckhunt is True:
                    if utfix(data[3]) is False:
                        continue
                    if func.cnfexists('duckhunt.cnf', 'flood_protection', str(data[3].decode()).replace(':', '')) is True:
                        woid = str(data[3].decode()).replace(':', '')
                        if woid.lower() == '\x01version\x01' or woid.lower() == '\x01finger\x01' or woid.lower() == '\x01ping':
                            flood = int(flood) + 4
                        elif woid.lower() == '!shop' and len(data) == 4:
                            flood = int(flood) + 4
                        elif woid.lower() == '!duckstats':
                            flood = int(flood) + 4
                        flood = int(flood) + 1
                        f_time = time.time() - float(flood_time)
                        cmds = func.gettok(func.cnfread('duckhunt.cnf', 'duckhunt', 'floodcheck'), 0, ',')
                        secs = func.gettok(func.cnfread('duckhunt.cnf', 'duckhunt', 'floodcheck'), 1, ',')
                        print('FLOOD COUNT: ' + str(flood) + ' FLOOD TIME: ' + str(round(f_time)))
                        if float(f_time) > float(secs) and int(flood) < int(cmds):
                            flood_time = time.time()
                            flood = 0
                        if int(flood) > int(cmds):
                            f_time = time.time() - float(flood_time)
                            if float(f_time) <= float(secs):
                                flood_cont = True
                                flood_timer = time.time()
                                irc.send(b'PRIVMSG ' + duckchan + b' :\x034* Flood Control Activated *\x03\r\n')
                                continue
                            if float(f_time) > float(secs):
                                flood_time = time.time()
                                flood = 0

# ======================================================================================================================
# CTCP VERSION, PING, FINGER
# ======================================================================================================================
                if data[2].lower() == botname.lower():
                    if data[3] == b":\x01VERSION\x01":
                        irc.send(b"NOTICE " + username + b' :\x01VERSION Super DuckHunt [Python Bot]: ' + botversion + b' by Neo_Nemesis' + b'\x01\r\n')
                        continue
                    if data[3] == b":\x01FINGER\x01":
                        irc.send(b"NOTICE " + username + b' :\x01FINGER Super DuckHunt [Python Bot]: ' + botversion + b' by Neo_Nemesis' + b'\x01\r\n')
                        continue
                    if data[3] == b":\x01PING":
                        irc.send(b"NOTICE " + username + b' :\x01PING ' + data[4] + b'\r\n')
                        continue
# ======================================================================================================================
# routine checks for duckhunt, timed items, and user ignore
# ======================================================================================================================
                # duckhunt is off, fix v 1.1.0
                if func.istok(botmaster, str(dusername), ',') == False and func.istok(adminlist, str(dusername), ',') == False and duckhunt == False:
                    time.sleep(0.5)
                    continue
                bot.iecheck(str(username))
                # botignore - update 1.1.0 fix
                if func.istok(botignore, str(dusername), ',') == True and botignore != '0':
                    if func.istok(botmaster, str(dusername), ',') == False and func.istok(adminlist, str(dusername), ',') == False:
                        continue
# ======================================================================================================================
# BOTMASTER AND ADMIN CONTROLS (PRIVMSG): /privmsg BotName <command> <parameters>
# ======================================================================================================================
                if data[2].lower() == botname.lower():

# relay <add/del/list> <relayname> =====================================================================================
#           /privmsg botname relay <add/del> <relayname> (botmaster only)
                    if data[3].lower() == b':relay' and func.istok(botmaster, dusername, ',') is True:
                        if len(data) == 5 and data[4].lower() == b'list':
                            relaybot = func.cnfread('duckhunt.cnf', 'duckhunt', 'relays')
                            if relaybot == '0':
                                irc.send(b'NOTICE ' + username + b' :The relay bot list is currently empty.\r\n')
                                continue
                            rbt = relaybot.replace(',', ' ')
                            irc.send(b'NOTICE ' + username + b' :Relay bot list: ' + rbt.encode() + b'\r\n')
                            continue
                        if len(data) == 6:
                            if data[4].lower() == b'add':
                                relaybot = func.cnfread('duckhunt.cnf', 'duckhunt', 'relays')
                                rb = data[5].decode()
                                if func.istok(relaybot, rb.lower(), ',') is True:
                                  irc.send(b'NOTICE ' + username + b' :' + data[5] + b' already exists in the relay bot list.\r\n')
                                  continue
                                if relaybot == '0':
                                    rb = data[5].decode()
                                    relaybot = rb.lower()
                                    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'relays', str(relaybot))
                                    irc.send(b'NOTICE ' + username + b' :' + data[5] + b' added to relay bot list.\r\n')
                                    continue
                                if relaybot != '0':
                                    rb = data[5].decode()
                                    relaybot = func.addtok(relaybot, str(rb).lower(), ',')
                                    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'relays', str(relaybot))
                                    irc.send(b'NOTICE ' + username + b' :' + data[5] + b' added to relay bot list.\r\n')
                                    continue
                            if data[4].lower() == b'del':
                                if data[5].lower() == b'all':
                                    relaybot = '0'
                                    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'relays', '0')
                                    irc.send(b'NOTICE ' + username + b' :Relay bot list has been cleared.\r\n')
                                    continue
                                rb = data[5].decode()
                                if func.istok(relaybot, rb.lower(), ',') is False:
                                    irc.send(b'NOTICE ' + username + b' :' + data[5] + b' is not listed in the relay bot list.\r\n')
                                    continue
                                if relaybot == rb.lower():
                                    relaybot = '0'
                                    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'relays', '0')
                                    irc.send(b'NOTICE ' + username + b' :' + data[5] + b' has been removed from the relay bot list.\r\n')
                                    continue
                                if func.istok(relaybot, rb.lower(), ',') is True:
                                    relaybot = func.deltok(relaybot, rb.lower(), ',')
                                    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'relays', str(relaybot))
                                    irc.send(b'NOTICE ' + username + b' :' + data[5] + b' has been removed from the relay bot list.\r\n')
                                    continue
                        continue
# boost <player> v 1.1.2 ===============================================================================================
#           /privmsg botname boost <player>
                    if data[3].lower() == b':boost' and len(data) == 5:
                        tusername = data[4].lower()
                        if func.istok(botmaster, str(dusername), ',') is False and func.istok(adminlist, str(dusername), ',') is False:
                            continue
                        if func.cnfexists('duckhunt.cnf', 'ducks', str(tusername)) is False:
                            irc.send(b'NOTICE ' + username + b' :' + tusername + b" hasn't played yet.\r\n")
                            continue
                        if bang == 'on':
                            ammo = bot.duckinfo(tusername, b'ammo')
                            mrounds = func.gettok(ammo, 2, '?')
                            rounds = mrounds
                            mags = func.gettok(ammo, 1, '?')
                            mmags = func.gettok(ammo, 3, '?')
                            ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
                            bot.duckinfo(str(tusername), b'ammo', str(ammo))
                            xp = bot.duckinfo(tusername, b'xp')
                            xp = int(xp) + 75
                            bot.duckinfo(str(tusername), b'xp', str(xp))
                            irc.send(b'NOTICE ' + username + b' :' + tusername + b' has received a boost. Rounds have been reloaded (1 mag) and 75 xp.\r\n')
                            irc.send(b'NOTICE ' + tusername + b' :You have received a boost. You were given: 1 full magazine and 75 xp from a admin or botmaster.\r\n')
                            continue
                        if bang == 'off':
                            breadbox = bot.duckinfo(tusername, b'bread')
                            mbread = func.gettok(breadbox, 0, '?')
                            bread = mbread
                            loaf = func.gettok(breadbox, 2, '?')
                            mloaf = func.gettok(breadbox, 3, '?')
                            breadbox = str(bread) + '?' + str(mbread) + '?' + str(loaf) + '?' + str(mloaf)
                            bot.duckinfo(tusername, b'bread', str(breadbox))
                            xp = bot.duckinfo(tusername, b'xp')
                            xp = int(xp) + 75
                            bot.duckinfo(str(tusername), b'xp', str(xp))
                            irc.send(b'NOTICE ' + username + b' :' + tusername + b' has received a boost. Bread has been reloaded (1 loaf) and 75 xp.\r\n')
                            irc.send(b'NOTICE ' + tusername + b' :You have received a boost. You were given: 1 loaf of bread and 75 xp from a admin or botmaster.\r\n')
                            continue
# maint <mode> =========================================================================================================
#           /privmsg BotName maint <mode> <data>
                    if data[3].lower() == b':maint' and func.istok(botmaster, str(dusername), ',') is True:
                        if len(data) >= 5:

                            # /privmsg BotName maint auto <0/12/X/24>
                            # Checks duckhunt.cnf for old or expired entries, removes them etc.
                            # set 0 to turn off, or specificy number from 12 to 24. (X)
                            #   /privmsg BotName maint auto 0 --> auto clean off
                            #   /privmsg BotName maint auto 12 --> auto on for every 12 hours
                            #   /privmsg BotName maint auto 24 --> auto on for every 24 hours.
                            if data[4].lower() == b'auto' and len(data) == 6:
                                data5 = data[5].decode()
                                if data5.isnumeric() == False or isinstance(data5, float) is True:
                                    irc.send(b'NOTICE ' + username + b' :Invalid request: auto value must be an integer from 12 to 72.\r\n')
                                    continue
                                if int(data5) == 0:
                                    if func.cnfread('duckhunt.cnf', 'duckhunt', 'maint') == '0':
                                        irc.send(b'NOTICE ' + username + b' :Auto maintenance is already off.\r\n')
                                        continue
                                    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'maint', '0')
                                    irc.send(b'NOTICE ' + username + b' :Auto maintenance has been turned off.\r\n')
                                    continue
                                if int(data5) < 12 or int(data5) > 72:
                                    irc.send(b'NOTICE ' + username + b' :Invalid request: auto maintenance value must be 12 to 72.\r\n')
                                    continue
                                func.cnfwrite('duckhunt.cnf', 'duckhunt', 'maint', str(data5))
                                irc.send(b'NOTICE ' + username + b' :Auto maintenance has ben turned on to run every ' + bytes(str(data5), 'utf-8') + b' hours.\r\n')
                                continue
                            # /privmsg botname maint do  (SEE <command> <data> below)
                            #   /privmsg botname maint do --> performs the regular maintenance procedure.
                            if data[4].lower() == b'do' and len(data) == 5:
                                irc.send(b'NOTICE ' + username + b' :Beginning maintenance, please wait...\r\n')
                                if duckhunt == True:
                                    duckhunt = False
                                irc.send(b'PRIVMSG ' + duckchan + b' :DuckHunt is temporarily off-line for bot maintenance. Please wait, this will only take a moment...\r\n')

                                bot.cnfcleanup()

                                if duckhunt == False:
                                    duckhunt = True
                                irc.send(b'PRIVMSG ' + duckchan + b' :Bot maintenance complete. DuckHunt is back on-line!\r\n')
                                irc.send(b'NOTICE ' + username + b' :Maintenance complete.\r\n')
                                continue
                            # /privmsg botname maint do <commands> <data>
                            if data[4].lower() == b'do' and len(data) > 5:
                                # /privmsg botname maint do user xp X
                                # removes all players with xp lesser than or equal to X.
                                if data[5].lower() == b'user' and len(data) == 8:
                                    if data[6].lower() == b'xp':
                                        data7 = data[7].decode()
                                        if data7.isnumeric() == False or isinstance(data7, float) is True:
                                            irc.send(b'NOTICE ' + username + b' :Invalid request. This value must be an integer.\r\n')
                                            continue
                                        irc.send(b'NOTICE ' + username + b' :Beginning maintenance, removing user entries with xp less than or equal to: ' + data[7] + b', please wait...\r\n')
                                        if duckhunt == True:
                                            duckhunt = False
                                        irc.send(b'PRIVMSG ' + duckchan + b' :DuckHunt is temporarily off-line for bot maintenance. Please wait, this will only take a moment...\r\n')

                                        bot.userdat('xp', str(data7))

                                        if duckhunt == False:
                                            duckhunt = True
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Bot maintenance complete. DuckHunt is back on-line!\r\n')
                                        irc.send(b'NOTICE ' + username + b' :Maintenance task complete.\r\n')
                                        continue
                                # /privmsg botname maint do user level X
                                if data[5].lower() == b'user' and len(data) == 8:
                                    if data[6].lower() == b'level':
                                        data7 = data[7].decode()
                                        if data7.isnumeric() is False or isinstance(data7, float) is True:
                                            irc.send(b'NOTICE ' + username + b' :Invalid request. This value must be an integer.\r\n')
                                            continue
                                        irc.send(b'NOTICE ' + username + b' :Beginning maintenance, removing user entries with level less than or equal to: ' + data[7] + b', please wait...\r\n')
                                        if duckhunt == True:
                                            duckhunt = False
                                        irc.send(b'PRIVMSG ' + duckchan + b' :DuckHunt is temporarily off-line for bot maintenance. Please wait, this will only take a moment...\r\n')

                                        bot.userdat('level', str(data7))

                                        if duckhunt == False:
                                            duckhunt = True
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Bot maintenance complete. DuckHunt is back on-line!\r\n')
                                        irc.send(b'NOTICE ' + username + b' :Maintenance task complete.\r\n')
                                        continue
# reset <mode> =========================================================================================================
#           /privmsg BotName reset <name> <data> --> reset functions (botmaster only)
                    if data[3].lower() == b':reset' and func.istok(botmaster, str(dusername), ',') is True:
                        if len(data) == 5:

                            # /privmsg BotName reset default --> restore bot settings to default
                            # RESETS EVERYTHING TO ORIGINAL STATE PLAYER DATA WILL BE LOST
                            # DOES NOT CHANGE: botname, botpass, botmaster/admin, server data, IRC data
                            if data[4].lower() == b'def' or data[4].lower() == b'default':
                                irc.send(b'NOTICE ' + username + b' :Resetting, please wait...\r\n')
                                if duckhunt == True:
                                    duckhunt = False
                                irc.send(b'PRIVMSG ' + duckchan + b' :DuckHunt is temporarily off-line for parameter changes. Please wait, this will only take a monent...\r\n')
                                time.sleep(0.10)
                                bot.resetdef()
                                time.sleep(0.10)
                                confiscatedguns = ''
                                jammedguns = ''
                                fear_factor = False
                                flood = 0
                                flood_time = time.time()
                                flood_cont = False
                                flood_timer = ''
                                duck = {}
                                duckid = ''
                                if duckhunt == False:
                                    duckhunt = True
                                top_shot()
                                time.sleep(0.10)
                                irc.send(b'PRIVMSG ' + duckchan + b' :Parameter changes complete. DuckHunt is back on-line!\r\n')
                                irc.send(b'NOTICE ' + username + b' :Reset complete.\r\n')
                                continue

                            # /privmsg BotName reset players --> resets player data only
                            if data[4].lower() == b'players':
                                irc.send(b'NOTICE ' + username + b' :Resetting, please wait...\r\n')
                                duckhunt = False
                                irc.send(b'PRIVMSG ' + duckchan + b' :DuckHunt is temporarily off-line for parameter changes. Please wait, this will only take a monent...\r\n')
                                time.sleep(0.10)
                                bot.statreset()
                                time.sleep(0.10)
                                irc.send(b'PRIVMSG ' + duckchan + b' :Parameter changes complete. DuckHunt is back on-line!\r\n')
                                irc.send(b'NOTICE ' + username + b' :Reset complete.\r\n')
                                continue

                            # /privmsg BotName reset totalshot --> resets total shots data only
                            if data[4].lower() == b'totalshot':
                                irc.send(b'NOTICE ' + username + b' :Resetting, please wait...\r\n')
                                bot.resetshot()
                                duckhunt = True
                                top_shot()
                                irc.send(b'NOTICE ' + username + b' :Reset complete.\r\n')
                                continue


                            # /privmsg BotName reset dual --> completely resets players and totalshot
                            if data[4].lower() == b'dual':
                                irc.send(b'NOTICE ' + username + b' :Resetting, please wait...\r\n')
                                if duckhunt == True:
                                    duckhunt = False
                                irc.send(b'PRIVMSG ' + duckchan + b' :DuckHunt is temporarily off-line for parameter changes. Please wait, this will only take a monent...\r\n')
                                time.sleep(0.10)
                                bot.statreset()
                                time.sleep(0.10)
                                bot.resetshot()
                                time.sleep(0.10)
                                if duckhunt == False:
                                    duckhunt = True
                                top_shot()
                                time.sleep(0.10)
                                irc.send(b'PRIVMSG ' + duckchan + b' :Parameter changes complete. DuckHunt is back on-line!\r\n')
                                irc.send(b'NOTICE ' + username + b' :Reset complete.\r\n')
                                continue

# rules <name> <data> ==================================================================================================
#           /privmsg BotName rules <name> <data>  --> toggle 'rules' on/off etc

                    if data[3].lower() == b':rules' and func.istok(botmaster, str(dusername), ',') is True:
                        if len(data) >= 6:
                    # /privmsg BotName rules infammo <on/off>
                            if data[4].lower() == b'infammo':
                                if data[5].lower() == b'on':
                                    if func.cnfread('duckhunt.cnf', 'rules', 'infammo') == 'on':
                                        irc.send(b'NOTICE ' + username + b' :Infinite ammo is already turned on.\r\n')
                                        continue
                                    func.cnfwrite('duckhunt.cnf', 'rules', 'infammo', 'on')
                                    infammo = 'on'
                                    irc.send(b'NOTICE ' + username + b' :Infinite ammo has been turned on.\r\n')
                                    continue
                                if data[5].lower() == b'off':
                                    if func.cnfread('duckhunt.cnf', 'rules', 'infammo') == 'off':
                                        irc.send(b'NOTICE ' + username + b' :Infinite ammo is already turned off.\r\n')
                                        continue
                                    func.cnfwrite('duckhunt.cnf', 'rules', 'infammo', 'off')
                                    infammo = 'off'
                                    irc.send(b'NOTICE ' + username + b' :Infinite ammo has been turned off.\r\n')
                                    continue
                    # /privmsg BotName rules gunconf <on/off>
                            if data[4].lower() == b'gunconf':
                                if data[5].lower() == b'on':
                                    if func.cnfread('duckhunt.cnf', 'rules', 'gunconf') == 'on':
                                        irc.send(b'NOTICE ' + username + b' :Gun confiscation is already turned on.\r\n')
                                        continue
                                    func.cnfwrite('duckhunt.cnf', 'rules', 'gunconf', 'on')
                                    gunconf = 'on'
                                    irc.send(b'NOTICE ' + username + b' :Gun confiscation has been turned on.\r\n')
                                    continue
                                if data[5].lower() == b'off':
                                    if func.cnfread('duckhunt.cnf', 'rules', 'gunconf') == 'off':
                                        irc.send(b'NOTICE ' + username + b' :Gun confiscation is already turned off.\r\n')
                                        continue
                                    func.cnfwrite('duckhunt.cnf', 'rules', 'gunconf', 'off')
                                    gunconf = 'off'
                                    irc.send(b'NOTICE ' + username + b' :Gun confiscation has been turned off.\r\n')
                                    continue
                    # /privmsg BotName rules gunricochet <0-100> (0 = off)
                            if data[4].lower() == b'gunricochet':
                                if data[5].lower() == b'0':
                                    if func.cnfread('duckhunt.cnf', 'rules', 'gunricochet') == '0':
                                        irc.send(b'NOTICE ' + username + b' :Bullet ricochet is already turned off.\r\n')
                                    func.cnfwrite('duckhunt.cnf', 'rules', 'gunricochet', '0')
                                    gunricochet = 0
                                    irc.send(b'NOTICE ' + username + b' :Bullet ricochet has been turned OFF at: 0%\r\n')
                                    continue
                                # set gunricochet N
                                data5 = data[5].decode()
                                if data5.isnumeric() is False or isinstance(str(data5), float) is True:
                                    irc.send(b'NOTICE ' + username + b' :Invalid request: Bullet ricochet value must be an integer.\r\n')
                                    continue
                                func.cnfwrite('duckhunt.cnf', 'rules', 'gunricochet', str(data5))
                                gunricochet = int(data5)
                                irc.send(b'NOTICE ' + username + b' :Bullet ricochet has been set to ON at: ' + bytes(str(data5), 'utf-8') + b'%.\r\n')
                                continue
                    # /privmsg BotName rules thebushes <0-100> (0 = off)
                            if data[4].lower() == b'thebushes':
                                data5 = data[5].decode()
                                if data5 == '0':
                                    if func.cnfread('duckhunt.cnf', 'rules', 'thebushes') == '0':
                                        irc.send(b'NOTICE ' + username + b' :Searching the bushes is already turned off.\r\n')
                                        continue
                                    func.cnfwrite('duckhunt.cnf', 'rules', 'thebushes', '0')
                                    thebushes = 0
                                    irc.send(b'NOTICE ' + username + b' :Searching the bushes has been turned OFF at: 0%\r\n')
                                    continue
                                if data5.isnumeric() == False or isinstance(data5, float) is True:
                                    irc.send(b'NOTICE ' + username + b' :Invalid request: Searching the bushes value must be an integer.\r\n')
                                    continue
                                func.cnfwrite('duckhunt.cnf', 'rules', 'thebushes', str(data5))
                                thebushes = int(data5)
                                irc.send(b'NOTICE ' + username + b' :Searching the bushes has been turned ON at: ' + bytes(str(data5), 'utf-8') + b'%\r\n')
                                continue

                    # /privmsg BotName rules bang <on/ff> ---> Enable or disable !bang (command set)
                    # botmaster only (command set: !bang, !reload and assosciated shop items
                            if data[4].lower() == b'bang' and func.istok(botmaster, str(dusername), ',') is True:
                                bang = func.cnfread('duckhunt.cnf', 'rules', 'bang')
                                if data[5].lower() == b'on':
                                    if bang == 'on':
                                        irc.send(b'NOTICE ' + username + b' :!bang command set is already enabled.\r\n')
                                        continue
                                    func.cnfwrite('duckhunt.cnf', 'rules', 'bang', 'on')
                                    bang = 'on'
                                    irc.send(b'NOTICE ' + username + b' :!bang command set has been enabled.\r\n')
                                    continue
                                if data[5].lower() == b'off':
                                    if bang == 'off':
                                        irc.send(b'NOTICE ' + username + b' :!bang command set is already disabled.\r\n')
                                        continue
                                    if bef == 'off':
                                        irc.send(b'NOTICE ' + username + b' :Invalid request: !bef command set is also turned off. First enable !bef, then try again.\r\n')
                                        continue
                                    func.cnfwrite('duckhunt.cnf', 'rules', 'bang', 'off')
                                    bang = 'off'
                                    irc.send(b'NOTICE ' + username + b' :!bang command set has been disabled.\r\n')
                                    continue

                    # /privmsg BotName rules bef <on/off> ---> Enable or disable !bef (command set)
                    # botmaster only (command set: !bef, !bread, and assosciated shop items
                            if data[4].lower() == b'bef' and func.istok(botmaster, str(dusername), ',') is True:
                                bef = func.cnfread('duckhunt.cnf', 'rules', 'bef')
                                if data[5].lower() == b'on':
                                    if bef == 'on':
                                        irc.send(b'NOTICE ' + username + b' :!bef command set is already enabled.\r\n')
                                        continue
                                    func.cnfwrite('duckhunt.cnf', 'rules', 'bef', 'on')
                                    irc.send(b'NOTICE ' + username + b' :!bef command set has been enabled.\r\n')
                                    bef = 'on'
                                    continue
                                if data[5].lower() == b'off':
                                    if bef == 'off':
                                        irc.send(b'NOTICE ' + username + b' :!bef command set is already disabled.\r\n')
                                        continue
                                    if bang == 'off':
                                        irc.send(b'NOTICE ' + username + b' :Invalid request: !bang command set is also turned off. First enable !bang, then try again.\r\n')
                                        continue
                                    func.cnfwrite('duckhunt.cnf', 'rules', 'bef', 'off')
                                    bef = 'off'
                                    irc.send(b'NOTICE ' + username + b' :!bef command set has been disabled.\r\n')
                                    continue

# do <commands> ========================================================================================================
#           /privmsg BotName do IRC PROTOCOLS (BOTMASTER ONLY)
#           /privmsg BotName do PRIVMSG #DuckHunt :Does at it's told!
                    # silent do command
                    if data[3].lower() == b':do' and func.istok(botmaster, str(dusername), ',') is True:
                        if len(data) == 4:
                            irc.send(b'NOTICE ' + username + b" :Does as it's told!\r\n")
                            continue
                        if len(data) > 4 and len(data) <= 6:
                            irc.send(b'NOTICE ' + username + b' :Invalid command request.\r\n')
                            continue
                        if len(data) > 6:
                            cmdstring = func.gettok(str(data), 1, ':do')
                            cmdstring = cmdstring.replace("b'", '')
                            cmdstring = cmdstring.replace("'", '')
                            cmdstring = cmdstring.replace(',', '')
                            cmdstring = cmdstring.replace(']', '')
                            cmdstring = cmdstring.replace(' PRIVMSG', 'PRIVMSG')
                            # print('DO: ' + str(cmdstring))
                            irc.send(bytes(str(cmdstring), 'utf-8') + b'\r\n')
                            continue
                        continue

# duckstats <username> =================================================================================================
#           /privmsg BotName duckstats <optional: username> ---> same as !duckstats but silent
                    # silent duckstats - (botmaster and admin)
                    if data[3].lower() == b':duckstats' and duckhunt is True:
                        if func.istok(botmaster, str(dusername), ',') is False and func.istok(adminlist, str(dusername), ',') is False:
                            continue
                        # duckstats
                        if len(data) == 4:
                            duckstats(username, username)
                            continue
                        # duckstats <username>
                        if len(data) == 5:
                            duckstats(username, data[4])
                            continue

# duckhunt <on/off> ====================================================================================================
#           /privmsg BotName duckhunt <on/off> --> turn DuckHunt on or off
                    # silent duckhunt on/off (botmaster only)
                    if data[3].lower() == b':duckhunt' and func.istok(botmaster, str(dusername), ',') is True:
                        if len(data) == 4:
                            irc.send(b'NOTICE ' + username + b' :Super DuckHunt is currently: ' + bytes(str(duckhunt), 'utf-8') + b'\r\n')
                            continue
                        if len(data) > 4:
                            if data[4].lower() == b'on':
                                if duckhunt is True:
                                    irc.send(b'NOTICE ' + username + b' :Super DuckHunt is already on.\r\n')
                                    continue
                                duckhunt = True
                                irc.send(b'NOTICE ' + username + b' :Super DuckHunt has been turned on.\r\n')
                                continue
                            if data[4].lower() == b'off':
                                if duckhunt is False:
                                    irc.send(b'NOTICE ' + username + b' :Super DuckHunt is already off.\r\n')
                                    continue
                                duckhunt = False
                                irc.send(b'NOTICE ' + username + b' :Super DuckHunt has been turned off.\r\n')
                                continue

# spawnduck <normal/golden> ============================================================================================
#           /privmsg BotName spawnduck <optional: normal/golden> --> spawn a duck
                    if data[3].lower() == b':spawnduck' and duckhunt is True:
                        if func.istok(botmaster, str(dusername), ',') is False and func.istok(adminlist, str(dusername),',') is False:
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

# del <admin/ignore/botmaster> <username> ==============================================================================
#           /privmsg botname del <admin/ignore/botmaster> <username> --> remove username
                    if data[3].lower() == b':del':
                        if func.istok(botmaster, str(dusername), ',') is False and func.istok(adminlist, str(dusername), ',') is False:
                            continue
                        if len(data) <= 4:
                            continue
                        # del admin <username>
                        if data[4].lower() == b'admin' and len(data) == 6 and func.istok(botmaster, str(dusername),
                                                                                         ',') is True:
                            data5 = data[5].decode()
                            adminlist = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin').lower()
                            if adminlist == '0' or func.istok(adminlist, str(data5), ',') == False:
                                irc.send(b'NOTICE ' + username + b' :Invalid request: User "' + bytes(str(data5), 'utf-8') + b'" does not exist in the admin list.\r\n')
                                continue
                            if func.numtok(adminlist, ',') == 1:
                                adminlist = '0'
                            if func.numtok(adminlist, ',') > 1:
                                adminlist = func.deltok(adminlist, str(data5), ',').lower()
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'admin', str(adminlist))
                            irc.send(b'NOTICE ' + username + b' :User ' + bytes(str(data5), 'utf-8') + b' removed from the admin list.\r\n')
                            continue
                        # del botmaster <username>
                        if data[4].lower() == b'botmaster' and len(data) == 6 and func.istok(botmaster, str(dusername),
                                                                                             ',') is True:
                            data5 = data[5].decode()
                            botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster').lower()
                            if func.numtok(botmaster, ',') == 1:
                                irc.send(
                                    b'NOTICE ' + username + b' :Invalid request: There must always be at least 1 botmaster.\r\n')
                                continue
                            botmaster = func.deltok(botmaster, str(data5).lower(), ',').lower()
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
                        if func.istok(botmaster, str(dusername), ',') == False and func.istok(adminlist, str(dusername), ',') == False:
                            continue
                        if len(data) <= 4:
                            continue
                        # add admin <username>
                        if data[4].lower() == b'admin' and len(data) == 6 and func.istok(botmaster, str(dusername),
                                                                                         ',') is True:
                            adminlist = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin').lower()
                            data5 = data[5].decode()
                            if func.istok(adminlist, data5, ',') is True:
                                irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5),
                                                                               'utf-8') + b' is already in the admin list.\r\n')
                                continue
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'admin') != '0':
                                adminlist = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin').lower()
                                adminlist = func.addtok(adminlist, str(data5), ',').lower()
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'admin') == '0':
                                adminlist = str(data5).lower()
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'admin', adminlist)
                            irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5),
                                                                           'utf-8') + b' has been added to the admin list.\r\n')
                            continue
                        # add botmaster <username>
                        if data[4].lower() == b'botmaster' and len(data) == 6 and func.istok(botmaster, str(dusername),
                                                                                             ',') is True:
                            botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster').lower()
                            data5 = data[5].decode()
                            if func.istok(botmaster, data5, ',') is True:
                                irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5),
                                                                               'utf-8') + b' is already in the botmaster list.\r\n')
                                continue
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster') != '0':
                                botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster').lower()
                                botmaster = func.addtok(botmaster, str(data5.lower()), ',').lower()
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster') == '0':
                                botmaster = str(data5).lower()
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'botmaster', botmaster)
                            irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5),
                                                                           'utf-8') + b' has been added to the botmaster list.\r\n')
                            continue
                        # add ignore <username>
                        if data[4].lower() == b'ignore' and len(data) == 6:
                            botignore = func.cnfread('duckhunt.cnf', 'duckhunt', 'ignore').lower()
                            data5 = data[5].decode()
                            if func.istok(botignore, data5, ',') is True:
                                irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5),
                                                                               'utf-8') + b' is already in the ignore list.\r\n')
                                continue
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'ignore') != '0':
                                botignore = func.cnfread('duckhunt.cnf', 'duckhunt', 'ignore').lower()
                                botignore = func.addtok(botignore, str(data5), ',').lower()
                            if func.cnfread('duckhunt.cnf', 'duckhunt', 'ignore') == '0':
                                botignore = str(data5).lower()
                            func.cnfwrite('duckhunt.cnf', 'duckhunt', 'ignore', botignore)
                            irc.send(b'NOTICE ' + username + b' :' + bytes(str(data5), 'utf-8') + b' has been added to the ignore list.\r\n')
                            continue
                        continue
# set <maxducks/spawntime/flytime/duckexp/duckfear/duckgold/friendrate> <value> ============================
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
                                irc.send(b'NOTICE ' + username + b' :The maxducks setting has been changed to: ' + bytes(str(data5), 'utf-8') + b' ducks.\r\n')
                                if duck_exists() and duckhunt == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b" :Due to a parameter change, the ducks in the area have flown away.     \x0314\xc2\xb7\xc2\xb0'`'\xc2\xb0-.,\xc2\xb8\xc2\xb8.\xc2\xb7\xc2\xb0'`\r\n")
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

                        # set flood <on/off> <msg,time>
                        # /privmsg BotName set flood on 10,8
                        # /privmsg BotName set flood off
                        if data[4].lower() == b'flood' and len(data) >= 4:
                            if len(data) == 5:
                                flc = func.cnfread('duckhunt.cnf', 'duckhunt', 'floodcheck')
                                if flc == '0':
                                    irc.send(b'NOTICE ' + username + b' :The flood protection is currently disabled.\r\n')
                                    continue
                                if flc != '0':
                                    det = func.cnfread('duckhunt.cnf', 'duckhunt', 'floodcheck')
                                    cmds = func.gettok(str(det), 0, ',')
                                    secs = func.gettok(str(det), 1, ',')
                                    irc.send(b'NOTICE ' + username + b' :The current flood protection settings are: ' + bytes(str(cmds), 'utf-8') + b' requests in: ' + bytes(str(secs), 'utf-8') + b' seconds.\r\n')
                                    continue

                            if data[5].lower() == b'on' and len(data) == 7 and func.numtok(str(data[6]), ',') == 2:
                                func.cnfwrite('duckhunt.cnf', 'duckhunt', 'floodcheck', str(data[6].decode()))
                                flood_check = True
                                cmds = func.gettok(str(data[6].decode()), 0, ',')
                                secs = func.gettok(str(data[6].decode()), 1, ',')
                                irc.send(b'NOTICE ' + username + b' :The flood protection settings have been changed to: ' + bytes(str(cmds), 'utf-8') + b' requests in: ' + bytes(str(secs), 'utf-8') + b' seconds.\r\n')
                                continue
                            if data[5].lower() == b'off':
                                flood_check = False
                                func.cnfwrite('duckhunt.cnf', 'duckhunt', 'floodcheck', '0')
                                irc.send(b'NOTICE ' + username + b' :The flood protection has been disabled.\r\n')
                                continue
                        continue
# ======================================================================================================================
# Parsing user name and data (for relay bots) v. 1.1.2
# ======================================================================================================================
                # if func.istok(relaybot, dusername, ',') is True:

# ======================================================================================================================
# Botmaster and Admin CHANNEL COMMANDS * *
# ======================================================================================================================
                if data[2].lower() == duckchan:
                    botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster').lower()
                    adminlist = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin').lower()
                    if func.istok(botmaster, dusername, ',') is True or func.istok(adminlist, dusername, ',') is True:
# ======================================================================================================================
# !exit (botmaster only)
# ======================================================================================================================
                        if data[3].lower() == b':!exit' or data3.lower() == b'!exit':
                            irc.send(b"PRIVMSG " + duckchan + b" :Shutting down...\r\n")
                            time.sleep(1)
                            irc.send(b"QUIT :Super DuckHunt Bot\r\n")
                            exitvar = True
                            exit()
# ======================================================================================================================
# !duckhunt <on/off> (Botmaster and Admin only)
# ======================================================================================================================
                        if data[3].lower() == b':!duckhunt' or data3.lower() == b'!duckhunt':
                            if len(data) != 5 or data4 == b'':
                                continue
                            if func.istok(botmaster, dusername, ',') is False and func.istok(adminlist, dusername, ',') is False:
                                continue
                            if data[4].lower() == b'on' or data4.lower() == b'on':
                                if duckhunt:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :Super DuckHunt is already turned on.\r\n')
                                    continue
                                elif not duckhunt:
                                    duckhunt = True
                                    irc.send(b'PRIVMSG ' + duckchan + b' :Super DuckHunt has been turned on.\r\n')
                                    continue
                            if data[4].lower() == b'off' or data4.lower() == b'off':
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

                    if data[3].lower() == b':!rules' or data3 == b'!rules':
                        confgun = 'Gun confiscation: ' + str(gunconf).upper()
                        ricogun = 'Bullets ricochet: ON'
                        if str(gunricochet) == '0':
                            ricogun = 'Bullets ricochet: OFF'
                        searchbush = 'Searching the bushes: ON'
                        if str(thebushes) == '0':
                            searchbush = 'Searching the bushes: OFF'
                        ammomode = 'Ammo supply: NORMAL'
                        if infammo == 'on':
                            ammomode = 'Ammo supply: INFINITE'
                        if bang == 'off':
                            ammomode = 'Bread supply: NORMAL'
                            if infammo == 'on':
                                ammomode = 'Bread supply: INFINITE'
                        gamemode = 'Game mode: NORMAL'
                        if bang == 'off':
                            gamemode = 'Game mode: NO GUNS'
                        if bef == 'off':
                            gamemode = 'Game mode: HUNTING ONLY'
                        if data3 == b'!rules' and datarelay == True:
                            irc.send(b'PRIVMSG ' + duckchan + b' :[' + duckchan + b' Super-DuckHunt In-Game Rules:] ' + confgun.encode() + b' | ' + ricogun.encode() + b' | ' + searchbush.encode() + b' | ' + ammomode.encode() + b' | ' + gamemode.encode() + b'\r\n')
                            continue
                        irc.send(b'NOTICE ' + username + b' :[' + duckchan + b' Super-DuckHunt In-Game Rules:] ' + confgun.encode() + b' | ' + ricogun.encode() + b' | ' + searchbush.encode() + b' | ' + ammomode.encode() + b' | ' + gamemode.encode() + b'\r\n')
                        continue
# ======================================================================================================================
# !shop [id] [target]
# shop purchases are controlled here
# ======================================================================================================================
                    if data[3].lower() == b':!shop' or data3 == b'!shop':
                        if func.cnfexists('duckhunt.cnf', 'ducks', str(username).lower()) == False:
                            if data3 == b'!shop' and datarelay == True:
                                irc.send(b'PRIVMSG ' + duckchan + b" :You can't use the shop yet because you haven't played. Shoot some ducks first.\r\n")
                                continue
                            irc.send(b'NOTICE ' + username + b" :You can't use the shop yet because you haven't played. Shoot some ducks first.\r\n")
                            continue
                        if len(data) == 4 and datarelay == False:
                            shopmenu(username)
                            continue
                        if len(data) > 4 and datarelay == True and data4 == b'':
                            shopmenu(username, 'opt')
                            continue
                        if len(data) >= 5:
                            if data4 != b'':
                                data4 = data4.decode()
                            if data4 == b'':
                                data4 = data[4].decode()
                            if not data4.isnumeric():
                                continue
                            itemid = int(data4)
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
                            loaf = func.gettok(breadbox, 2, '?')
                            mloaf = func.gettok(breadbox, 3, '?')
# not enough xp to purchase ============================================================================================
                            if int(xp) < bot.shopprice(username, itemid):
                                if data3 == b'!shop' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You do not have enough xp for this purchase.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You do not have enough xp for this purchase.\r\n')
                                continue
# checks if user is on the channel, and prevents users from targeting themselves =======================================
                            if len(data) >= 6 or datarelay == True:
                                if datarelay == True and data4 == b'':
                                    continue
                                if int(itemid) == 14 or int(itemid) == 15 or int(itemid) == 16 or int(itemid) == 17:
                                    if bang == 'off':
                                        if int(itemid) == 15 or int(itemid) == 17:
                                            if data5 != b'' and datarelay == True:
                                                irc.send(b'PRIVMSG ' + duckchan + b' :Based on current rules this item is not available.\r\n')
                                                continue
                                            irc.send(b'NOTICE ' + username + b' :Based on current rules this item is not available.\r\n')
                                            continue
                                    # can't use it on the bot
                                    if str(data[5].lower()) == str(botname.lower()) or str(data5.lower()) == str(botname.lower()):
                                        if data5 != b'' and datarelay == True:
                                            irc.send(b'PRIVMSG ' + duckchan + b' :Nice try ;-)\r\n')
                                            continue
                                        irc.send(b'NOTICE ' + username + b' :Nice try ;-)\r\n')
                                        continue
                                    # user isn't on the channel/hasn't played yet
                                    # (recoded this section for relay bots) v1.1.3
                                    # relay bot players
                                    if datarelay == True:
                                        if data5 == b'':
                                            continue
                                        if func.cnfexists('duckhunt.cnf', 'ducks', str(data5.lower())) == False:
                                            irc.send(b'PRIVMSG ' + duckchan + b' :' + data5 + b" hasn't played yet.\r\n")
                                            continue
                                        print('here ' + str(data5.lower()))
                                        if namecheck(str(data5.decode())) == False and bot.duckinfo(str(data5.lower()), b'inv') == '0':
                                            irc.send(b'PRIVMSG ' + duckchan + b' :' + data5 + b' is not in the channel.\r\n')
                                            continue
                                    # normal players v1.1.3
                                    if datarelay == False:
                                        if func.cnfexists('duckhunt.cnf', 'ducks', str(data[5].lower())) == False:
                                            irc.send(b'NOTICE ' + username + b' :' + data[5] + b" hasn't played yet.\r\n")
                                            continue
                                        if namecheck(str(data[5].decode())) == False and bot.duckinfo(str(data[5].lower()), b'inv') == '0':
                                            irc.send(b'NOTICE ' + username + b' :' + data[5] + b' is not in the channel.\r\n')
                                            continue
                                    # can't use it on yourself
                                    if str(data[5].lower()) == str(username.lower()) or datarelay == True:
                                        if datarelay == True and str(data5.lower()) == str(username.lower()):
                                            irc.send(b'PRIVMSG ' + duckchan + b" :Don't do that to yourself!\r\n")
                                            continue
                                        if datarelay != True and str(data[5].lower()) == str(username.lower()):
                                            irc.send(b'NOTICE ' + username + b" :Don't do that to yourself!\r\n")
                                            continue
# 1 - single bullet ====================================================================================================
                            if int(itemid) == 1:
                                # infammo is on
                                if infammo == 'on' or bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                # can't hold any more
                                if rounds == mrounds:
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You cannot carry any more bullets.\r\n')
                                        continue
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
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased a single bullet.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased a single bullet.\r\n')
                                continue
# 2 - refill magazine ==================================================================================================
                            if int(itemid) == 2:
                                # infammo is on
                                if infammo == 'on' or bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                # can't hold anymore
                                if mags == mmags:
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :All your magazines are full.\r\n')
                                        continue
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
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You refilled 1 magazine.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You refilled 1 magazine.\r\n')
                                continue
# 3 - gun cleaning =====================================================================================================
                            # update 1.1.0 moved from #6 to #3
                            if int(itemid) == 3:
                                if bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                # gun doesn't need to be cleaned
                                if reliability == mreliability:
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b" :Your gun doesn't need to be cleaned.\r\n")
                                        continue
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
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b" :Your gun is now cleaned and reliability is restored to maximum.\r\n")
                                    continue
                                irc.send(b'NOTICE ' + username + b" :Your gun is now cleaned and reliability is restored to maximum.\r\n")
                                continue
# 4 - explosive ammo v 1.1.0 ===========================================================================================
                            if int(itemid) == 4:
                                if bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                bot.data_check(username, 'expl_ammo')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'expl_ammo', str(username)):
                                    useleft = func.cnfread('duckhunt.cnf', 'expl_ammo', str(username))
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You already own Explosive Ammo. [Rounds left: ' + bytes(str(useleft), 'utf-8') + b']\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You already own Explosive Ammo. [Rounds left: ' + bytes(str(useleft), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # apply rounds 50 rounds
                                func.cnfwrite('duckhunt.cnf', 'expl_ammo', str(username), '50')
                                # confirmation
                                if data4 == b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You bought 50 rounds of Explosive Ammo. Increased damage. These rounds are 15% more likely to hit their targets.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You bought 50 rounds of Explosive Ammo. Increased damage. These rounds are 15% more likely to hit their targets.\r\n')
                                continue
# 5 - return confiscated gun ===========================================================================================
                            if int(itemid) == 5:
                                # update 1.1.0 - gun confiscation on/off
                                if gunconf == 'off' or bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                # not confiscated
                                if confiscatedguns == '':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Your gun is not currently confiscated.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Your gun is not currently confiscated.\r\n')
                                    continue
                                if func.istok(confiscatedguns, str(username), ',') == False:
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Your gun is not currently confiscated.\r\n')
                                        continue
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
                                if data4 == b'' and datarelay == True:
                                    irc.send(b'NOTICE ' + username + b' :Your confiscated gun has been returned.\r\n')
                                irc.send(b'PRIVMSG ' + duckchan + b' :\x01ACTION returns ' + username + b"'s gun to them.\x01\r\n")
                                continue
# 6 - gun grease =======================================================================================================
                            # update 1.1.0 moved from #3 to #6
                            if int(itemid) == 6:
                                if bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                bot.data_check(str(username), 'gun_grease')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'gun_grease', str(username)) is True:
                                    # 24 hour timer calculation
                                    timeleft = bot.data_check(str(username.lower()), 'gun_grease', 'get')
                                    # (timeleft)
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You already own Gun Grease. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b']\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You already own Gun Grease. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # shop purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'gun_grease', str(username), str(time.time()))
                                # purchase confirmation
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased Gun Grease. Lower jamming odds and gun reliability will last longer for 24 hours.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased Gun Grease. Lower jamming odds and gun reliability will last longer for 24 hours.\r\n')
                                continue
# 7 - gun upgrade ======================================================================================================
                            if int(itemid) == 7:
                                if bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                # can't upgrade anymore/fully upgraded
                                if str(accuracy) == '100' and str(mreliability) == '100':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Your gun is already fully upgraded.\r\n')
                                        continue
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
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You have upgraded your gun. Accuracy and reliability have increased.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You have upgraded your gun. Accuracy and reliability have increased.\r\n')
                                continue
# 8 - Gun Lock =====================================================================================================
                            # update 1.1.0 - removed 24 hours and replaced with limitation based on max rounds
                            # max rounds = number of Gun Locks - price changed, will vary based on max rounds
                            if int(itemid) == 8:
                                if bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                bot.data_check(username, 'trigger_lock')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'trigger_lock', str(username)) == True:
                                    useleft = bot.data_check(str(username), 'trigger_lock', 'get')
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You already own Gun Lock. [Remaining Use: ' + bytes(str(useleft), 'utf-8') + b']\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You already own Gun Lock. [Remaining Use: ' + bytes(str(useleft), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # add entry for max rounds
                                func.cnfwrite('duckhunt.cnf', 'trigger_lock', str(username), str(mrounds))
                                # purchase confirmation
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased Gun Lock. The gun will have a safety lock when no ducks are sighted for ' + bytes(str(mrounds), 'utf-8') + b' uses.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased Gun Lock. The gun will have a safety lock when no ducks are sighted for ' + bytes(str(mrounds), 'utf-8') + b' uses.\r\n')
                                continue
# 9 - silencer =========================================================================================================
                            if int(itemid) == 9:
                                if bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                bot.data_check(username, 'silencer')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'silencer', str(username)) == True:
                                    # 24 hour timer calculation
                                    timeleft = bot.data_check(str(username), 'silencer', 'get')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You already own Silencer. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b']\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You already own Silencer. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'silencer', str(username), str(time.time()))
                                # purchase confirmation
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased a Silencer for your gun. You will not scare away ducks for 24 hours.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased a Silencer for your gun. You will not scare away ducks for 24 hours.\r\n')
                                continue
# 10 - lucky charm =====================================================================================================
                            # update 1.1.0 - changed from double xp to 3-10 random for 24 hours
                            if int(itemid) == 10:
                                bot.data_check(username, 'lucky_charm')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)) == True:
                                    # 24 hour timer calculation
                                    timeleft = func.gettok(bot.data_check(str(username), 'lucky_charm', 'get'), 0, ',')
                                    lcxp = func.gettok(bot.data_check(str(username), 'lucky_charm', 'get'), 1, ',')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You already own Lucky Charm. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b' +' + bytes(str(lcxp), 'utf-8') + b' xp]\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You already own Lucky Charm. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b' +' + bytes(str(lcxp), 'utf-8') + b' xp]\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                lcxp = random.randint(3,10)
                                func.cnfwrite('duckhunt.cnf', 'lucky_charm', str(username), str(time.time()) + ',' + str(lcxp))
                                # purchase confirmation
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased a Lucky Charm. You will earn an extra ' + bytes(str(lcxp), 'utf-8') + b' xp for 24 hours.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased a Lucky Charm. You will earn an extra ' + bytes(str(lcxp), 'utf-8') + b' xp for 24 hours.\r\n')
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
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You already own Sunglasses. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b']\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You already own Sunglasses. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # cannot buy sunglasses if currently bedazzled.
                                if func.cnfexists('duckhunt.cnf', 'bedazzled', str(username)) == True:
                                    # add 1 hour timer stuff
                                    timeleft = bot.data_check(str(username), 'bedazzled', 'get')
                                    timemath = func.hour1() - math.ceil(time.time() - float(timeleft))
                                    timemath = bot.timeconvertmsg(timemath)
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You are currently bedazzled and have to wait for it to wear off to use Sunglasses. [Time Remaining: ' + bytes(str(timemath), 'utf-8') + b']\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You are currently bedazzled and have to wait for it to wear off to use Sunglasses. [Time Remaining: ' + bytes(str(timemath), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'sunglasses', str(username), str(time.time()))
                                # purchase confirmation
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased Sunglasses. You are protected from bedazzlement for 24 hours.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased Sunglasses. You are protected from bedazzlement for 24 hours.\r\n')
                                continue
# 12 - new clothes =====================================================================================================
                            # update 1.1.0 - added stuff for duck bombs
                            if int(itemid) == 12:
                                # not soggy or bombed
                                if func.cnfexists('duckhunt.cnf', 'soggy', str(username)) is False and func.cnfexists('duckhunt.cnf', 'bombed', str(username)) is False:
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Your clothes are not wet or dirty.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Your clothes are not wet or dirty.\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # remove soggy
                                if func.cnfexists('duckhunt.cnf', 'soggy', str(username)):
                                    func.cnfdelete('duckhunt.cnf', 'soggy', str(username))
                                # remove bombed
                                if func.cnfexists('duckhunt.cnf', 'bombed', str(username)):
                                    func.cnfdelete('duckhunt.cnf', 'bombed', str(username))
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased New Clothes. You are no longer soggy and/or duck bombed.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased New Clothes. You are no longer soggy and/or duck bombed.\r\n')
                                continue
# 13 - eyedrops v 1.1.0 ================================================================================================
                            if int(itemid) == 13:
                                # not bedazzled
                                if not func.cnfexists('duckhunt.cnf', 'bedazzled', str(username)):
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You are not currently bedazzled.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You are not currently bedazzled.\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # remove bedazzled
                                func.cnfdelete('duckhunt.cnf', 'bedazzled', str(username))
                                # confirmation
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased Eye Drops. You are no longer bedazzled.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased Eye Drops. You are no longer bedazzled.\r\n')
                                continue
# 14 - mirror ==========================================================================================================
                            if int(itemid) == 14:
                                targetname = b''
                                if len(data) < 6:
                                    continue
                                if datarelay == True:
                                    targetname = data5
                                if datarelay == False:
                                    targetname = data[5]
                                bot.data_check(targetname, 'bedazzled')
                                bot.data_check(targetname, 'sunglasses')
                                # target already bedazzled
                                if func.cnfexists('duckhunt.cnf', 'bedazzled', str(targetname)) == True:
                                    if datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + targetname + b' is already bedazzled.\r\n')
                                        continue
                                    if datarelay == False:
                                        irc.send(b'NOTICE ' + username + b' :' + targetname + b' is already bedazzled.\r\n')
                                        continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # target wearing sunglasses!
                                if func.cnfexists('duckhunt.cnf', 'sunglasses', str(targetname)) == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Bedazzles ' + targetname + b', with a mirror, but ' + targetname + b' is wearing sunglasses so the mirror has no effect.\r\n')
                                    continue
                                # target not wearing sunglasses
                                if func.cnfexists('duckhunt.cnf', 'sunglasses', str(targetname)) == False:
                                    # adding time entry (1 hours)
                                    func.cnfwrite('duckhunt.cnf', 'bedazzled', str(targetname), str(time.time()))
                                    # confirmation
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Bedazzles ' + targetname + b' with a mirror who is now blinded for 1 hour.\r\n')
                                    continue
# 15 - handful of sand =================================================================================================
                            if int(itemid) == 15:
                                targetname = b''
                                if len(data) < 6:
                                    continue
                                if bang == 'off':
                                    if datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                # purchase
                                if datarelay == True:
                                    targetname = data5
                                if datarelay == False:
                                    targetname = data[5]
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # reliability reduction
                                tgunstats = bot.duckinfo(targetname, b'guninfo')
                                taccuracy = func.gettok(tgunstats, 0, '?')
                                treliability = func.gettok(tgunstats, 1, '?')
                                tmreliability = func.gettok(tgunstats, 2, '?')
                                # effects - apply
                                if float(treliability) < 5:
                                    treliability = 0
                                if float(treliability) >= 5:
                                    treliability = float(treliability) - 5
                                tgunstats = str(taccuracy) + '?' + str(treliability) + '?' + str(tmreliability)
                                bot.duckinfo(targetname, b'guninfo', str(tgunstats))
                                # confirmation
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Pours a handful of sand into ' + targetname + b"'s gun, reducing its reliability by 5%.\r\n")
                                continue
# 16 - water bucket ====================================================================================================
                            if int(itemid) == 16:
                                targetname = b''
                                if len(data) < 6:
                                    continue
                                if datarelay == False:
                                    targetname = data[5]
                                if datarelay == True and data5 != b'':
                                    targetname = data5
                                bot.data_check(targetname, 'soggy')
                                bot.data_check(targetname, 'rain_coat')
                                # target is already soggy
                                if func.cnfexists('duckhunt.cnf', 'soggy', str(targetname)) == True:
                                    if datarelay == True and targetname != b'':
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + targetname + b' is already soggy.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :' + targetname + b' is already soggy.\r\n')
                                    continue
                                # target has a rain coat
                                if func.cnfexists('duckhunt.cnf', 'rain_coat', str(targetname)) == True:
                                    # purchase
                                    xp = int(xp) - bot.shopprice(username, itemid)
                                    bot.duckinfo(username, b'xp', str(xp))
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Dumps a bucket of water on ' + targetname + b', but thanks to a rain coat, ' + targetname + b' is protected from being soggy.\r\n')
                                    continue
                                # target not wearing a rain coat
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'soggy', str(targetname), str(time.time()))
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # confirmation
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Dumps a bucket of water on ' + targetname + b'. ' + targetname + b' is now soggy for 1 hour.\r\n')
                                continue
# 17 - sabotage ========================================================================================================
                            if int(itemid) == 17:
                                targetname = b''
                                if len(data) < 6:
                                    continue
                                if datarelay == True:
                                    targetname = data5
                                if datarelay == False:
                                    targetname = data[5]
                                if bang == 'off':
                                    if datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                # target already sabotaged
                                if func.cnfexists('duckhunt.cnf', 'sabotage', str(targetname.lower())) == True:
                                    if datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + targetname + b"'s gun is already sabotaged.\r\n")
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :' + targetname + b"'s gun is already sabotaged.\r\n")
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # target effects apply - lasts 1 shot
                                func.cnfwrite('duckhunt.cnf', 'sabotage', str(targetname), str(True))
                                # confirmation
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Sabotages the gun while ' + targetname + b" isn't looking.\r\n")
                                continue
# 18 - accident insurance ==============================================================================================
                            # update 1.1.0 - accident insurance now increases lost xp +4 in exchange for no confiscation
                            if int(itemid) == 18:
                                # update 1.1.0 - gun confiscation on/off
                                if gunconf == 'off' or bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                bot.data_check(username, 'accident_insurance')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)) == True:
                                    # 24 hour timer calculation
                                    timeleft = bot.data_check(str(username), 'accident_insurance', 'get')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You already own Accident Insurance. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b']\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You already own Accident Insurance. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'accident_insurance', str(username), str(time.time()))
                                # confirmation
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased Accident Insurance. This will prevent gun confiscation for 24 hours.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased Accident Insurance. This will prevent gun confiscation for 24 hours.\r\n')
                                continue
# 19 - bread - "ammo" for befriending ducks ============================================================================
                            # update 1.1.0 - changed and expanded bread to carry more than 1 loaf
                            if int(itemid) == 19:
                                # infammo is on
                                if infammo == 'on' or bef == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue

                                # !bef disabled
                                # if bef == 'off':
                                #    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                #    continue

                                # bread box is full
                                if int(loaf) == int(mloaf):
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Your bread box is full.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Your bread box is full.\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # apply bread refill
                                loaf = int(loaf) + 1
                                breadbox = str(bread) + '?' + str(mbread) + '?' + str(loaf) + '?' + str(mloaf)
                                bot.duckinfo(username, b'bread', str(breadbox))
                                # confirmation
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased 1 loaf of bread.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased 1 loaf of bread.\r\n')
                                continue
# 20 - bag of popcorn - increased befriending v 1.1.0 ==================================================================
                            if int(itemid) == 20:
                                if bef == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                bot.data_check(username, 'popcorn')
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'popcorn', str(username)):
                                    popc = func.cnfread('duckhunt.cnf', 'popcorn', str(username))
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You already have a bag of popcorn. [Remaining pieces: ' + bytes(str(popc), 'utf-8') + b']\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You already have a bag of popcorn. [Remaining pieces: ' + bytes(str(popc), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # apply popcorn ammo
                                func.cnfwrite('duckhunt.cnf', 'popcorn', str(username), '50')
                                # confirmation
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased a Bag of Popcorn. You can now have better luck at befriending ducks for 50 pieces.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased a Bag of Popcorn. You can now have better luck at befriending ducks for 50 pieces.\r\n')
                                continue
# 21 - bread box lock - trigger lock for !bef v 1.1.0 ==================================================================
                            if int(itemid) == 21:
                                if bef == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'bread_lock', str(username)):
                                    useleft = func.cnfread('duckhunt.cnf', 'bread_lock', str(username))
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You already own Bread Box Lock. [Remaining uses: ' + bytes(str(useleft), 'utf-8') + b']\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You already own Bread Box Lock. [Remaining uses: ' + bytes(str(useleft), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # apply bread box lock
                                func.cnfwrite('duckhunt.cnf', 'bread_lock', str(username), str(mbread))
                                # confirmation
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased Bread Box Lock. You can not toss bread when no ducks are around for' + bytes(str(mbread), 'utf-8') + b' uses.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased Bread Box Lock. You can not toss bread when no ducks are around for' + bytes(str(mbread), 'utf-8') + b' uses.\r\n')
                                continue
# 22 - rain coat - prevents soggy and duck bombing =====================================================================
                            if int(itemid) == 22:
                                bot.data_check(username, 'soggy')
                                bot.data_check(username, 'rain_coat')
                                # currently soggy
                                if func.cnfexists('duckhunt.cnf', 'soggy', str(username)) == True:
                                    # 1 hour timer calculation
                                    timeleft = bot.data_check(username, 'soggy', 'get')
                                    timemath = func.hour1() - math.ceil(time.time() - float(timeleft))
                                    timemath = bot.timeconvertmsg(timemath)
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You are currently soggy and cannot purchase Rain Coat until you are dry. [Time Remaining: ' + bytes(str(timemath), 'utf-8') + b']\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You are currently soggy and cannot purchase Rain Coat until you are dry. [Time Remaining: ' + bytes(str(timemath), 'utf-8') + b']\r\n')
                                    continue
                                # already own this item
                                if func.cnfexists('duckhunt.cnf', 'rain_coat', str(username)) == True:
                                    # 24 hour timer calculation
                                    timeleft = bot.data_check(str(username), 'rain_coat', 'get')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You already own Rain Coat. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b']\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You already own Rain Coat. [Time Remaining: ' + bytes(str(timeval), 'utf-8') + b']\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # adding time entry (24 hours)
                                func.cnfwrite('duckhunt.cnf', 'rain_coat', str(username), str(time.time()))
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased Rain Coat. This will protect against water buckets and duck bombs for 24 hours.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased Rain Coat. This will protect against water buckets and duck bombs for 24 hours.\r\n')
                                continue

# 23 - magazine upgrade =================================================================================================
                            if int(itemid) == 23:
                                if bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                # magazines cannot be upgraded any further (max upgrade already reached)
                                if int(mrounds) == 12:
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Your magazines are already fully upgraded, and cannot be upgraded further.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Your magazines are already fully upgraded, and cannot be upgraded further.\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                # apply upgrade
                                mrounds = int(mrounds) + 1
                                ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
                                bot.duckinfo(username, b'ammo', str(ammo))
                                # confirmation
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You upgraded your magazines! They can now hold ' + bytes(str(mrounds), 'utf-8') + b' rounds.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You upgraded your magazines! They can now hold ' + bytes(str(mrounds), 'utf-8') + b' rounds.\r\n')
                                continue
# 24 - additional magazine =============================================================================================
                            if int(itemid) == 24:
                                # infammo is on
                                if infammo == 'on' or bang == 'off':
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :Based on current game rules, this item is not available.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :Based on current game rules, this item is not available.\r\n')
                                    continue
                                # can't carry any more
                                if int(mmags) == 5:
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :You cannot carry anymore additional magazines.\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b' :You cannot carry anymore additional magazines.\r\n')
                                    continue
                                # purchase
                                xp = int(xp) - bot.shopprice(username, itemid)
                                bot.duckinfo(username, b'xp', str(xp))
                                mmags = int(mmags) + 1
                                ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
                                bot.duckinfo(username, b'ammo', str(ammo))
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You purchased an additional magazine, you can now carry ' + bytes(str(mmags), 'utf-8') + b' magazines.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You purchased an additional magazine, you can now carry ' + bytes(str(mmags), 'utf-8') + b' magazines.\r\n')
                                continue
                            # end of shop
                            continue
# ======================================================================================================================
# !swim - update v1.1.0
# ======================================================================================================================
                    if data[3].lower() == b':!swim' or data3.lower() == b'!swim':
                        # haven't played yet
                        if not func.cnfexists('duckhunt.cnf', 'ducks', str(username)):
                            if data3 != b'' and datarelay == True:
                                irc.send(b'PRIVMSG ' + duckchan + b" :You haven't played yet. Shoot some ducks first.\r\n")
                                continue
                            irc.send(b'NOTICE ' + username + b" :You haven't played yet. Shoot some ducks first.\r\n")
                            continue

                        # set data
                        xp = bot.duckinfo(username, b'xp')
                        level = bot.duckinfo(username, b'level')

                        # deterimine xp subtract
                        rxp = 2
                        if int(xp) >= 10000 or int(level) >= 10:
                            rxp = 12
                        elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                            rxp = 8
                        elif int(xp) < 5000 and int(xp) >= 1500:
                            rxp = 4
                        # deduct xp
                        if int(rxp) >= int(xp):
                            xp = 0
                            bot.duckinfo(username, b'xp', str(xp))
                        if int(rxp) < int(xp):
                            xp = int(xp) - int(rxp)
                            bot.duckinfo(username, b'xp', str(xp))
                        # apply soggy
                        func.cnfwrite('duckhunt.cnf', 'soggy', str(username), str(time.time()))
                        # wash duck bomb off
                        if func.cnfexists('duckhunt.cnf', 'bombed', str(username)):
                            func.cnfdelete('duckhunt.cnf', 'bombed', str(username))
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Jumps into the duck pond, and rinses off the duck bombs, but ' + username + b' is now soggy for 1 hour \x034[-' + bytes(str(rxp), 'utf-8') + b' xp]\r\n')
                            continue
                        # confirmation
                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Decides to jump in the duck pond. What are you doing? ' + username + b' is now soggy for 1 hour \x034[-' + bytes(str(rxp), 'utf-8') + b' xp]\r\n')
                        continue
# ======================================================================================================================
# !bomb recode v1.1.0
# ======================================================================================================================
                    if data[3].lower() == b':!bomb' or data3.lower() == b'!bomb':
                        if len(data) == 5 or data4 != b'':

                            # user hasn't played
                            if func.cnfexists('duckhunt.cnf', 'ducks', str(username)) == False:
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(username), 'utf-8') + b' > You have not played yet.\r\n')
                                continue

                            # recently hit limit within last 24 hours
                            if func.cnfexists('duckhunt.cnf', 'duck_bomb', str(username)):
                                bombent = func.gettok(func.cnfread('duckhunt.cnf', 'duck_bomb', str(username)), 1, ',')
                                if int(bombent) == 0:
                                    timeleft = func.gettok(func.cnfread('duckhunt.cnf', 'duck_bomb', str(username)), 0, ',')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b" :You've recently used your limit of duck bombings within the last 24 hours. Try again in: " + bytes(str(timeval), 'utf-8') + b'\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b" :You've recently used your limit of duck bombings within the last 24 hours. Try again in: " + bytes(str(timeval), 'utf-8') + b'\r\n')
                                    continue

                            # not enough duck friends
                            friend = bot.duckinfo(str(username), b'friend')
                            if int(friend) < 50:
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You do not have enough duck friends to this. For 1 duck bomb you need 50 duck friends. You currently have: ' + bytes(str(friend), 'utf-8') + b' duck friends.\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :You do not have enough duck friends to this. For 1 duck bomb you need 50 duck friends. You currently have: ' + bytes(str(friend), 'utf-8') + b' duck friends.\r\n')
                                continue

                            # can't bomb the bot
                            if data[4].lower() == botname.lower() or data4.lower() == botname.lower():
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :Nice try. ;-)\r\n')
                                    continue
                                irc.send(b'NOTICE ' + username + b' :Nice try. ;-)\r\n')
                                continue

                            # target hasn't played (relay bots v1.1.3)
                            if not func.cnfexists('duckhunt.cnf', 'ducks', str(data4.lower())) and data4 != b'' and datarelay == True:
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > ' + data4 + b' has not played yet.\r\n')
                                continue
                            # target hasn't played
                            if not func.cnfexists('duckhunt.cnf', 'ducks', str(data[4].lower())) and data4 == b'' and datarelay == False:
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > ' + data[4] + b' has not played yet.\r\n')
                                continue

                            # can't bomb yourself
                            if str(data[4].lower()) == str(username.lower()) or str(data4.lower()) == str(username.lower()):
                                if data4 != b'' and datarelay == True:
                                    irc.send(b'PRIVMSG ' + duckchan + b" :Don't do that to yourself!\r\n")
                                    continue
                                irc.send(b'NOTICE ' + username + b" :Don't do that to yourself!\r\n")
                                continue

                            # user isn't on the channel (relay bots v1.1.3)
                            if not namecheck(str(data4.decode())) and data4 != b'' and datarelay == True and bot.duckinfo(str(data4.lower()), b'inv') == '0':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > ' + data4 + b' is not in the channel.\r\n')
                                continue
                            # user isn't on the channel
                            if not namecheck(str(data[4].decode())) and datarelay == False and bot.duckinfo(str(data[4].lower()), b'inv') == '0':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > ' + data[4] + b' is not in the channel.\r\n')
                                continue

                            # target is already bombed (relay bots v1.1.3)
                            if func.cnfexists('duckhunt.cnf', 'bombed', str(data4).lower()) == True and datarelay == True:
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(data4.decode()), 'utf-8') + b' is currently bombed.\r\n')
                                continue
                            # target is already bombed
                            if func.cnfexists('duckhunt.cnf', 'bombed', str(data[4]).lower()) == True and datarelay == False:
                                irc.send(b'NOTICE ' + username + b' :' + bytes(str(data[4].decode()), 'utf-8') + b' is currently bombed.\r\n')
                                continue
                            # determine duck bombs
                            # check if user duck bombing limit in last 24 hours
                            friend = bot.duckinfo(username, b'friend')
                            bot.data_check(str(username.lower()), 'duck_bomb')

                            if func.cnfexists('duckhunt.cnf', 'duck_bomb', str(username.lower())):
                                bombent = func.gettok(func.cnfread('duckhunt.cnf', 'duck_bomb', str(username)), 1, ',')
                                # user at limit of duck bombs in 24 hours
                                if int(bombent) == 0:
                                    timeleft = func.gettok(func.cnfread('duckhunt.cnf', 'duck_bomb', str(username)), 0, ',')
                                    timemath = func.hour24() - (math.ceil(time.time()) - float(timeleft))
                                    timeval = bot.timeconvertmsg(timemath)
                                    if data4 != b'' and datarelay == True:
                                        irc.send(b'PRIVMSG ' + duckchan + b" :You've recently used your limit of duck bombings within the last 24 hours. Try again in: " + bytes(str(timeval), 'utf-8') + b'\r\n')
                                        continue
                                    irc.send(b'NOTICE ' + username + b" :You've recently used your limit of duck bombings within the last 24 hours. Try again in: " + bytes(str(timeval), 'utf-8') + b'\r\n')
                                    continue
                                if int(bombent) > 0:
                                    bombent = int(bombent) - 1
                                    func.cnfwrite('duckhunt.cnf', 'duck_bomb', str(username), str(time.time()) + ',' + str(bombent))

                            if not func.cnfexists('duckhunt.cnf', 'duck_bomb', str(username)):
                                if int(friend) >= 50 and int(friend) < 100:
                                    func.cnfwrite('duckhunt.cnf', 'duck_bomb', str(username), str(time.time()) + ',0')
                                if int(friend) >= 100 and int(friend) < 150:
                                    func.cnfwrite('duckhunt.cnf', 'duck_bomb', str(username), str(time.time()) + ',1')
                                if int(friend) >= 150 and int(friend) < 200:
                                    func.cnfwrite('duckhunt.cnf', 'duck_bomb', str(username), str(time.time()) + ',2')
                                if int(friend) >= 200 and int(friend) < 300:
                                    func.cnfwrite('duckhunt.cnf', 'duck_bomb', str(username), str(time.time()) + ',3')
                                if int(friend) >= 300 and int(friend) < 400:
                                    func.cnfwrite('duckhunt.cnf', 'duck_bomb', str(username), str(time.time()) + ',4')
                                if int(friend) >= 400 and int(friend) < 1000:
                                    func.cnfwrite('duckhunt.cnf', 'duck_bomb', str(username), str(time.time()) + ',5')
                                if int(friend) >= 1000:
                                    func.cnfwrite('duckhunt.cnf', 'duck_bomb', str(username), str(time.time()) + ',10')

                            bombent = func.gettok(func.cnfread('duckhunt.cnf', 'duck_bomb', str(username)), 1, ',')

                            # target has rain coat (relay bots v1.1.3)
                            if data4 != b'' and datarelay == True:
                                bot.data_check(str(data4.lower()), 'rain_coat')
                                # target does not have rain coat
                                if not func.cnfexists('duckhunt.cnf', 'rain_coat', str(data4.lower())):
                                    func.cnfwrite('duckhunt.cnf', 'bombed', str(data4.lower()), str(True))
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Calls in a duck bombing on ' + data4 + b'. A squadron of 50 duck friends, flying in formation, swoop down dropping gooey duck bombs all over ' + data4 + b' causing the player to require new clothes!\r\n')
                                if func.cnfexists('duckhunt.cnf', 'rain_coat', str(data4.lower())):
                                    func.cnfdelete('duckhunt.cnf', 'rain_coat', str(data4.lower()))
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Calls in a duck bombing on ' + data4 + b' A squadron of 50 duck friends, flying in formation, swoop down dropping duck bombs all over ' + data4 + b'. Thanks to a Rain Coat ' + data4 + b' is shielded from the duck bombs, but can no longer use this Rain Coat.\r\n')

                                if int(bombent) == 0:
                                    irc.send(b'PRIVMSG ' + duckchan + b" :You've reached the limit of your duck bombs. They will be replenished in 24 hours.\r\n")
                                    continue
                                if int(bombent) == 1:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You have 1 duck bomb left and 24 hours to use it.\r\n')
                                    continue
                                if int(bombent) > 0:
                                    irc.send(b'PRIVMSG ' + duckchan + b' :You have: ' + bytes(str(bombent), 'utf-8') + b' duck bombs left and 24 hours to use one.\r\n')
                                    continue
                                continue

                            # normal rain coat
                            bot.data_check(str(data[4].lower()), 'rain_coat')
                            # does not have rain coat
                            if not func.cnfexists('duckhunt.cnf', 'rain_coat', str(data[4].lower())):
                                func.cnfwrite('duckhunt.cnf', 'bombed', str(data[4].lower()), str(True))
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Calls in a duck bombing on ' + data[4] + b'. A squadron of 50 duck friends, flying in formation, swoop down dropping gooey duck bombs all over ' + data[4] + b' causing the player to require new clothes!\r\n')
                            # has rain coat
                            if func.cnfexists('duckhunt.cnf', 'rain_coat', str(data[4].lower())):
                                func.cnfdelete('duckhunt.cnf', 'rain_coat', str(data[4].lower()))
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Calls in a duck bombing on ' + data[4] + b' A squadron of 50 duck friends, flying in formation, swoop down dropping duck bombs all over ' + data[4] + b'. Thanks to a Rain Coat ' + data[4] + b' is shielded from the duck bombs, but can no longer use this Rain Coat.\r\n')

                            if int(bombent) == 0:
                                irc.send(b'NOTICE ' + username + b" :You've reached the limit of your duck bombs. They will be replenished in 24 hours.\r\n")
                                continue
                            if int(bombent) == 1:
                                irc.send(b'NOTICE ' + username + b' :You have 1 duck bomb left and 24 hours to use it.\r\n')
                                continue
                            if int(bombent) > 0:
                                irc.send(b'NOTICE ' + username + b' :You have: ' + bytes(str(bombent), 'utf-8') + b' duck bombs left and 24 hours to use one.\r\n')
                                continue
                            continue

# ======================================================================================================================
# !lastduck
# update 1.1.0 - added if duck exists message (a duck currently exists!)
# ======================================================================================================================
                    if data[3].lower() == b':!lastduck' or data3.lower() == b'!lastduck':
                        if duck_exists():
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > There is currently a duck in the area, fire!\r\n')
                            continue
                        last_time = time.time() - float(start_time)
                        mesg = bot.timeconvertmsg(last_time)
                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > The last duck was seen: ' + bytes(str(mesg), 'utf-8') + b' ago.\r\n')
                        continue
# ======================================================================================================================
# !topduck
# ======================================================================================================================
                    if data[3].lower() == b':!topduck' or data3.lower() == b'!topduck':
                        topduck()
                        continue
# ======================================================================================================================
# !duckstats <optional user name>
# ======================================================================================================================
                    if data[3].lower() == b':!duckstats' or data3.lower() == b'!duckstats':
                        if len(data) == 4 or data3 != b'':
                            if datarelay == True and data4 == b'':
                                # For relay bots v1.1.3
                                duckstats(username, username, 'opt')
                                continue
                            if datarelay == False:
                                duckstats(username, username)
                                continue
                        if len(data) == 5 or data4 != b'':
                            if data4 != b'' and datarelay == True:
                                # For relay bots v1.1.3
                                duckstats(username, data4, 'opt')
                                continue
                            if datarelay == False:
                                duckstats(username, data[4])
                                continue
# ======================================================================================================================
# !rearm <all, optional user name>
# !rearm - rearms yourself.
# Channel OPs/Bot Access/Bot Master only
# ======================================================================================================================
                    if data[3].lower() == b':!rearm' or data3.lower() == b'!rearm':
                        if bang == 'off':
                            continue
                        if func.istok(botmaster, str(dusername), ',') == False and func.istok(adminlist, str(dusername), ',') == False:
                            continue
                        # !rearm
                        if len(data) == 4 or data3 != b'':
                            if func.istok(confiscatedguns, str(username), ',') == False and data4 == b'':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Your gun is not confiscated.\r\n')
                                continue
                            if func.numtok(confiscatedguns, ',') == 1:
                                confiscatedguns = ''
                            if func.numtok(confiscatedguns, ',') > 1:
                                confiscatedguns = func.deltok(confiscatedguns, str(username), ',')
                            if data3 != b'' and data4 == b'':
                                irc.send(b'PRIVMSG ' + duckchan + b' :\x01ACTION returns ' + username + b"'s gun.\x01\r\n")
                                continue
                            irc.send(b'PRIVMSG ' + duckchan + b' :\x01ACTION returns ' + username + b"'s gun.\x01\r\n")
                            continue
                        # !rearm <username> and !rearm all
                        if len(data) == 5 or data4 != b'':
                            if data[4] == b'all' or data4 == b'all':
                                confiscatedguns = ''
                                irc.send(b'PRIVMSG ' + duckchan + b' :\x01ACTION returns all confiscated guns to the hunters.\x01\r\n')
                                continue
                            if func.istok(confiscatedguns, str(data[4]), ',') == False and datarelay == False:
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + data[4] + b"'s gun is not confiscated.\r\n")
                                continue
                            if datarelay == True and data4 != b'' and func.istok(confiscatedguns, str(data4), ',') == False:
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + data4 + b"'s gun is not confiscated.\r\n")
                                continue
                            if func.numtok(confiscatedguns, ',') == 1:
                                confiscatedguns = ''
                            if func.numtok(confiscatedguns, ',') > 1:
                                confiscatedguns = func.deltok(confiscatedguns, str(username), ',')
                            if data4 != b'':
                                irc.send(b'PRIVMSG ' + duckchan + b' :\x01ACTION returns ' + data4 + b"'s gun.\x01\r\n")
                                continue
                            irc.send(b'PRIVMSG ' + duckchan + b' :\x01ACTION returns ' + data[4] + b"'s gun.\x01\r\n")
                            continue
# ======================================================================================================================
# !reload
# ======================================================================================================================
                    if data[3].lower() == b':!reload' or data3.lower() == b'!reload':
                        if bang == 'off':
                            continue
                        # check if players gun is confiscated
                        gunconf = func.cnfread('duckhunt.cnf', 'rules', 'gunconf')
                        if func.istok(confiscatedguns, str(username), ',') == True and gunconf == 'on':
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x034You are not armed.\x03\r\n')
                            continue
                        # unjam gun
                        if func.istok(jammedguns, str(username), ',') == True:
                            if func.numtok(jammedguns, ',') == 1:
                                jammedguns = ''
                            if func.numtok(jammedguns, ',') > 1:
                                jammedguns = func.deltok(jammedguns, str(username), ',')
                            func.cnfwrite('duckhunt.cnf', 'duck_jam', str(username), '0')
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x0314*Crr..CLICK*\x03     You unjam your gun.\r\n")
                            continue
                        # new users with no stats, gun doesn't need to be reloaded
                        if func.cnfexists('duckhunt.cnf', 'ducks', str(username)) == False:
                            if infammo == 'on':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > Your gun doesn't need to be reloaded. | Rounds: 7/7 | Magazines: \x02\x033Inf\x02\x03\r\n")
                            if infammo == 'off':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > Your gun doesn't need to be reloaded. | Rounds: 7/7 | Magazines: 3/3\r\n")
                            continue
                        # reloading gun
                        rounds = func.gettok(bot.duckinfo(username, b'ammo'), 0, '?')
                        mags = func.gettok(bot.duckinfo(username, b'ammo'), 1, '?')
                        mrounds = func.gettok(bot.duckinfo(username, b'ammo'), 2, '?')
                        mmags = func.gettok(bot.duckinfo(username, b'ammo'), 3, '?')
                        if int(rounds) == 0:
                            # out of magazines
                            if int(mags) == 0 and infammo == 'off':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034You are out of magazines.\x03 | Rounds:\x034 0\x03/" + mrounds.encode() + b" | Magazines:\x034 0\x03/" + mmags.encode() + b'\r\n')
                                continue
                            # successful reload
                            if infammo == 'off':
                                mags = int(mags) - 1
                                mags = str(mags)
                            rounds = mrounds
                            ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
                            bot.duckinfo(username, b'ammo', ammo)
                            if infammo == 'on':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x0314*CLACK CLACK*\x03     You reload. | Rounds: " + rounds.encode() + b'/' + mrounds.encode() + b' | Magazines: \x02\x033Inf\x02\x03\r\n')
                            if infammo == 'off':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x0314*CLACK CLACK*\x03     You reload. | Rounds: " + rounds.encode() + b'/' + mrounds.encode() + b' | Magazines: ' + mags.encode() + b'/' + mmags.encode() + b'\r\n')
                            continue
                        # gun doesn't need to be reloaded
                        if int(rounds) > 0:
                            if infammo == 'on':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > Your gun doesn't need to be reloaded. | Rounds: " + rounds.encode() + b'/' + mrounds.encode() + b' | Magazines: \x02\x033Inf\x02\x03\r\n')
                            if infammo == 'off':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > Your gun doesn't need to be reloaded. | Rounds: " + rounds.encode() + b'/' + mrounds.encode() + b' | Magazines: ' + mags.encode() + b'/' + mmags.encode() + b'\r\n')
                            continue
# ======================================================================================================================
# !bang recode v1.1.0
# ======================================================================================================================
                    if data[3].lower() == b':!bang' or data3.lower() == b'!bang':
                        if bang == 'off':
                            continue

                        # bangresult = bangshot(username)
                        # print('USER: ' + str(username))
                        # print('BANG result: ' + str(bangresult))

                        # new users with no stats
                        # b'playername' = Rounds?Mags?MaxRounds?MaxMags,Ducks,GoldenDucks,xp,level,levelup,
                        #                 notusedanymore,notusedanymore,Accuracy?Reliability?MaxReliability,BestTime,
                        #                 Accidents,Bread?MaxBread,Loaf,MaxLoaf,DuckFriends
                        if not func.cnfexists('duckhunt.cnf', 'ducks', str(username)):
                            dinfo = '7?3?7?3,0,0,0,1,200,0,0,75?80?80,0,0,12?12?3?3,0'
                            func.cnfwrite('duckhunt.cnf', 'ducks', str(username), str(dinfo))
                            func.cnfwrite('duckhunt.cnf', 'ducks', 'cache', '1')

                        # gun is confiscated
                        gunconf = func.cnfread('duckhunt.cnf', 'rules', 'gunconf')
                        if func.istok(confiscatedguns, str(username), ',') and gunconf == 'on':
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x034You are not armed.\x03\r\n')
                            continue

                        # player is bombed
                        if func.cnfexists('duckhunt.cnf', 'bombed', str(username).lower()):
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x034Your clothes are crusty and filthy from being duck bombed. You cannot hunt ducks like this, you need new clothes.\r\n')
                            continue

                        # player is soggy
                        bot.data_check(username, 'soggy')
                        if func.cnfexists('duckhunt.cnf', 'soggy', str(username)):
                            # determine time remaining
                            # 1 hour timer calculation
                            timeleft = bot.data_check(str(username), 'soggy', 'get')
                            timemath = func.hour1() - math.ceil(time.time() - float(timeleft))
                            timemath = bot.timeconvertmsg(timemath)
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034Your clothes are all soggy. You cannot hunt ducks until you're dry. \x033[Time Remaining: " + bytes(str(timemath), 'utf-8') + b']\x03\r\n')
                            continue

                        # player is sabotaged
                        if func.cnfexists('duckhunt.cnf', 'sabotage', str(username).lower()) and func.cnfexists('duckhunt.cnf', 'trigger_lock', str(username).lower()) == False:
                            func.cnfdelete('duckhunt.cnf', 'sabotage', str(username).lower())
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*CLICK PFFFFT*\x03     \x034Your gun was sabotaged.\x03\r\n')
                            continue

                        # shooting data
                        ammo = bot.duckinfo(username, b'ammo')
                        rounds = func.gettok(ammo, 0, '?')
                        mrounds = func.gettok(ammo, 2, '?')
                        mags = func.gettok(ammo, 1, '?')
                        mmags = func.gettok(ammo, 3, '?')

                        guninfo = bot.duckinfo(username, b'guninfo')
                        accuracy = func.gettok(guninfo, 0, '?')
                        reliability = func.gettok(guninfo, 1, '?')
                        mreliability = func.gettok(guninfo, 2, '?')

                        xp = bot.duckinfo(username, b'xp')
                        best = bot.duckinfo(username, b'best')
                        ducks = bot.duckinfo(username, b'ducks')
                        gducks = bot.duckinfo(username, b'gducks')
                        accidents = bot.duckinfo(username, b'accidents')
                        level = bot.duckinfo(username, b'level')
                        levelup = bot.duckinfo(username, b'levelup')

                        # player gun needs service
                        if float(reliability) <= 60:
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*CLICK-CLACK*\x03     \x034Your gun is too dirty and needs to be cleaned...\x03\r\n')
                            continue

                        # empty magazine
                        if int(rounds) == 0:
                            if infammo == 'on':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*CLICK*\x03     \x034EMPTY MAGAZINE\x03 | Rounds:\x034 ' + rounds.encode() + b'\x03/' + mrounds.encode() + b' | Magazines: \x02\x033Inf\x02\x03\r\n')
                            if infammo == 'off':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*CLICK*\x03     \x034EMPTY MAGAZINE\x03 | Rounds:\x034 ' + rounds.encode() + b'\x03/' + mrounds.encode() + b' | Magazines: ' + mags.encode() + b'/' + mmags.encode() + b'\r\n')
                            continue

                        # Gun Lock
                        bot.data_check(str(username), 'trigger_lock')
                        if func.cnfexists('duckhunt.cnf', 'trigger_lock', str(username)) == True and duck_exists() == False:
                            useleft = func.cnfread('duckhunt.cnf', 'trigger_lock', str(username))
                            if int(useleft) == 1:
                                useleft = '0'
                                func.cnfdelete('duckhunt.cnf', 'trigger_lock', str(username))
                            if int(useleft) > 1:
                                useleft = int(useleft) - 1
                                func.cnfwrite('duckhunt.cnf', 'trigger_lock', str(username), str(useleft))
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*CLICK*\x03    \x034GUN LOCKED   [' + bytes(str(useleft), 'utf-8') + b']\x03\r\n')
                            continue

                        # jammed gun
                        if not func.cnfexists('duckhunt.cnf', 'duck_jam', str(username)) or func.istok(jammedguns, str(username), ','):
                            # gun grease update 1.1.0 - added lower jamming odds to gun grease (reliability +10)
                            #                           and adjusted jamming parameters to reduce frequent jamming
                            bot.data_check(str(username), 'gun_grease')
                            jam = round(float(reliability))
                            jammed = random.randint(1, 100)

                            if int(jam) <= 70 and int(jam) > 60:
                                if func.cnfexists('duckhunt.cnf', 'gun_grease', str(username)):
                                    jam = jam + 13
                                    jammed = random.randint(1, int(jam))
                                if not func.cnfexists('duckhunt.cnf', 'gun_grease', str(username)):
                                    jam = jam + 25
                                    jammed = random.randint(1, int(jam))

                            if jammed >= float(reliability) or func.istok(jammedguns, str(username), ',') is True:
                                if jammedguns == b'':
                                    jammedguns = str(username)
                                else:
                                    jammedguns = str(jammedguns) + ',' + str(username)
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*CLACK*\x03     \x034Your gun is jammed, you must reload to unjam it...\x03\r\n')
                                continue

                        # not jammed
                        if func.cnfexists('duckhunt.cnf', 'duck_jam', str(username)):
                            func.cnfdelete('duckhunt.cnf', 'duck_jam', str(username))

                        # fired a round
                        rounds = int(rounds) - 1

                        # ammo deduction
                        ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
                        bot.duckinfo(username, b'ammo', ammo)

                        # has expl ammo
                        bot.data_check(str(username), 'expl_ammo')
                        if func.cnfexists('duckhunt.cnf', 'expl_ammo', str(username)):
                            expammo = func.cnfread('duckhunt.cnf', 'expl_ammo', str(username))
                            if int(expammo) > 0:
                                expammo = int(expammo) - 1
                                func.cnfwrite('duckhunt.cnf', 'expl_ammo', str(username), str(expammo))
                                # extra wear for ammo type
                                reliability = float(reliability) - 0.03

                        # Reliability deduction
                        bot.data_check(str(username), 'gun_grease')

                        # does not have gun grease
                        if not func.cnfexists('duckhunt.cnf', 'gun_grease', str(username)):
                            reliability = float(reliability) - 0.1

                        # has gun grerase
                        if func.cnfexists('duckhunt.cnf', 'gun_grease', str(username)):
                            reliability = float(reliability) - 0.01

                        reliability = round(reliability, 2)
                        guninfo = str(accuracy) + '?' + str(reliability) + '?' + str(mreliability)
                        bot.duckinfo(username, b'guninfo', guninfo)

                        # duck exists
                        if duck_exists():

                            # duck fear management
                            bot.data_check(username, 'silencer')
                            if not func.cnfexists('duckhunt.cnf', 'silencer', str(username)):

                                if not fear_factor:
                                    fear_factor = 0
                                # scared the ducks away
                                if fear_factor >= duckfear:
                                    fl = 1
                                    while fl <= maxducks:
                                        duckid = 'd' + str(fl)
                                        duck[duckid] = 'None'
                                        fl += 1
                                        continue
                                    irc.send(b'PRIVMSG ' + duckchan + b" :\x034Frightened by so much noise, all ducks in the area have fled.\x03     \x0314\xc2\xb7\xc2\xb0'`'\xc2\xb0-.,\xc2\xb8\xc2\xb8.\xc2\xb7\xc2\xb0'`\r\n")
                                    fear_factor = False
                                    gold_factor = False
                                    continue
                                # ducks not scared
                                if fear_factor < duckfear:
                                    scare = random.randrange(2, 8, 1)
                                    fear_factor = fear_factor + scare

                            # check if player is bedazzled
                            bot.data_check(username, 'bedazzled')
                            if func.cnfexists('duckhunt.cnf', 'bedazzled', str(username)):
                                # player is bedazzled
                                accidents = int(accidents) + 1
                                bot.duckinfo(username, b'accidents', str(accidents))

                                damage = ''
                                dmg = random.randint(1, 3)

                                # determine xp subtract
                                rxp = dmg
                                if int(xp) >= 10000:
                                    rxp = dmg * 2
                                if int(xp) >= 5000 and int(xp) < 10000:
                                    rxp = dmg + 3
                                if int(xp) < 5000 and int(xp) >= 1500:
                                    rxp = dmg + 1

                                # gunconf off is off, extra -xp - v1.1.0
                                if gunconf == 'off':
                                    rxp = rxp + 4

                                # deduct xp
                                if int(xp) <= rxp:
                                    xp = 0
                                if int(xp) > rxp:
                                    xp = int(xp) - rxp
                                bot.duckinfo(username, b'xp', str(xp))

                                # determine accident
                                if dmg == 1:
                                    damage = 'Shot a distant window!'
                                if dmg == 2:
                                    damage = 'Shot another hunter!'
                                if dmg == 3:
                                    damage = 'Wildfire!'

                                # gunconf turned off update 1.1.0
                                if gunconf == 'off':
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x034     Missed due to being bedazzled. [-' + str(rxp).encode() + b' xp] [' + bytes(str(damage), 'utf-8') + b']\x03\r\n')
                                    continue

                                # determine accident insurance
                                bot.data_check(username, 'accident_insurance')
                                # has accident insurance
                                if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):

                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x034     Missed due to being bedazzled. [-' + str(rxp).encode() + b' xp] \x033[GUN NOT CONFISCATED: Accident Insurance]\x03\r\n')
                                    continue
                                # does not have accident insurance
                                if not func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                    # gun confiscation
                                    if confiscatedguns != '':
                                        confiscatedguns = str(confiscatedguns) + ',' + str(username)
                                    if confiscatedguns == '':
                                        confiscatedguns = str(username)

                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x034     Missed due to being debazzled. [-' + str(rxp).encode() + b' xp] [GUN CONFISCATED: ' + damage.encode() + b']\x03\r\n')
                                    continue

                            # determine duck
                            duckdata = ''
                            duck_time = ''
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

                            # normal duck
                            # if func.gettok(duckdata, 1, ',') == 'normal':
                            hitormiss = random.randrange(1, 100, 1)
                            # normal-gold duck
                            if func.gettok(duckdata, 1, ',') == 'gold':
                                hitormiss = random.randrange(0, 200, 1)
                            # golden duck
                            if func.gettok(duckdata, 1, ',') == 'golden':
                                hitormiss = random.randrange(0, 125, 1)

                            # expl ammo adds +15 accuracy
                            if func.cnfexists('duckhunt.cnf', 'expl_ammo', str(username)):
                                hitormiss = int(hitormiss) - 15

                            # missed
                            if hitormiss > int(accuracy):

                                # ricochet here
                                ricochet = random.randint(1, 100)
                                if int(ricochet) < int(gunricochet) and int(gunricochet) > 0:

                                    # accidents
                                    accidents = int(accidents) + 1
                                    bot.duckinfo(username, 'accidents', accidents)
                                    # determine damage
                                    damage = ''
                                    dmg = random.randint(1, 3)
                                    if dmg == 1:
                                        damage = 'strikes a distant window!'
                                    if dmg == 2:
                                        damage = 'strikes another hunter!'
                                    if dmg == 3:
                                        damage = 'starts a wildfire!'

                                    # determine xp subtract
                                    rxp = dmg
                                    if int(xp) >= 10000:
                                        rxp = dmg * 2
                                    if int(xp) >= 5000 and int(xp) < 10000:
                                        rxp = dmg + 3
                                    if int(xp) < 5000 and int(xp) >= 1500:
                                        rxp = dmg + 1

                                    # gunconf is off
                                    if gunconf == 'off':
                                        # deduct xp
                                        rxp = rxp + 4
                                        if int(xp) <= rxp:
                                            xp = 0
                                        if int(xp) > rxp:
                                            xp = int(xp) - rxp
                                        bot.duckinfo(username, str(xp))
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(str(damage), 'utf-8') + b' \x034[-' + str(dmg).encode() + b' xp] [Ricochet]\x03\r\n')
                                        continue
                                    # determine accident insurance
                                    bot.data_check(username, 'accident_insurance')

                                    # has accident insurance
                                    if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                        # deduct xp
                                        rxp = rxp + 4
                                        if int(xp) <= rxp:
                                            xp = 0
                                        if int(xp) > rxp:
                                            xp = int(xp) - rxp
                                        bot.duckinfo(username, str(xp))
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username+ b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(str(damage), 'utf-8') + b' \x034[-' + str(dmg).encode() + b' xp]\x03 \x033[GUN NOT CONFISCATED: Accident Insurance]\x03\r\n')
                                        continue
                                    # does not have accident insurance
                                    if not func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                        # deduct xp
                                        if int(xp) <= rxp:
                                            xp = 0
                                        if int(xp) > rxp:
                                            xp = int(xp) - rxp
                                        bot.duckinfo(username, str(xp))
                                        # gun confiscation
                                        if confiscatedguns != '':
                                            confiscatedguns = str(confiscatedguns) + ',' + str(username)
                                        if confiscatedguns == '':
                                            confiscatedguns = str(username)
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(str(damage), 'utf-8') + b' \x034[-' + str(dmg).encode() + b' xp] [GUN CONFISCATED: Ricochet]\x03\r\n')
                                        continue

                                # normal duck miss
                                if func.gettok(duckdata, 1, ',') == 'normal':
                                    # determine xp tier
                                    if int(xp) >= 10000 or int(level) >= 10:
                                        rxp = 7
                                    elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                                        rxp = 5
                                    elif int(xp) < 5000 and int(xp) >= 1500:
                                        rxp = 2
                                    else:
                                        rxp = 1
                                    # deduct xp
                                    if int(xp) <= int(rxp):
                                        xp = 0
                                        bot.duckinfo(username, b'xp', str(xp))
                                    if int(xp) > int(rxp):
                                        xp = int(xp) - int(rxp)
                                        bot.duckinfo(username, b'xp', str(xp))

                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03     \x034MISSED   [-' + str(rxp).encode() + b' xp]\x03\r\n')
                                    continue

                                # normal-gold miss
                                if func.gettok(duckdata, 1, ',') == 'gold':
                                    # determine xp tier
                                    if int(xp) >= 10000 or int(level) >= 10:
                                        rxp = 7
                                    elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                                        rxp = 5
                                    elif int(xp) < 5000 and int(xp) >= 1500:
                                        rxp = 2
                                    else:
                                        rxp = 1
                                    # deduct xp
                                    if int(xp) <= int(rxp):
                                        xp = 0
                                        bot.duckinfo(username, b'xp', str(xp))
                                    if int(xp) > int(rxp):
                                        xp = int(xp) - int(rxp)
                                        bot.duckinfo(username, b'xp', str(xp))

                                    # first miss, not golden yet
                                    if func.numtok(duckdata, ',') == 2:
                                        duckdata = duckdata + ',1'
                                        duck[duckid] = duckdata

                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03     \x034MISSED   [-' + str(rxp).encode() + b' xp]\x03\r\n')
                                        continue

                                    # determine if duck will turn golden
                                    if int(func.gettok(duckdata, 2, ',')) >= 1:
                                        duckstat = random.randrange(3, 4, 1)
                                        duckdata = func.gettok(duckdata, 0, ',') + ',golden,' + str(duckstat)
                                        duck[duckid] = duckdata

                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03     \x034MISSED   [-' + str(rxp).encode() + b' xp]\x037   \x02\\_O<    * GOLDEN DUCK DETECTED *\x02\x03\r\n')
                                        continue

                                    if int(func.gettok(duckdata, 2, ',')) < 1:
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03     \x034MISSED   [-' + str(rxp).encode() + b' xp]\x03\r\n')
                                        continue

                                # golden miss
                                if func.gettok(duckdata, 1, ',') == 'golden':
                                    # determine xp tier
                                    if int(xp) >= 10000 or int(level) >= 10:
                                        rxp = 8
                                    elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                                        rxp = 6
                                    elif int(xp) < 5000 and int(xp) >= 1500:
                                        rxp = 4
                                    else:
                                        rxp = 2
                                    # deduct xp
                                    if int(xp) <= int(rxp):
                                        xp = 0
                                        bot.duckinfo(username, b'xp', str(xp))
                                    if int(xp) > int(rxp):
                                        xp = int(xp) - int(rxp)
                                        bot.duckinfo(username, b'xp', str(xp))

                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03     \x034MISSED   [-' + str(rxp).encode() + b' xp]\x03\r\n')
                                    continue

                            # hit
                            if hitormiss <= int(accuracy):

                                #  normal ducks
                                if func.gettok(duckdata, 1, ',') == 'normal':
                                    # top shot counter
                                    bot.tshotplus()
                                    # reaction time determination
                                    reacttime = round(time.time() - float(duck_time), 2)
                                    if best == '0':
                                        bot.duckinfo(username, b'best', str(reacttime))
                                    if float(best) > reacttime:
                                        bot.duckinfo(username, b'best', str(reacttime))
                                    # increase ducks
                                    ducks = int(ducks) + 1
                                    bot.duckinfo(username, b'ducks', str(ducks))
                                    # increase xp
                                    bot.data_check(username, 'lucky_charm')
                                    # does not have lucky charm
                                    if not func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                        exp = duckexp
                                        xp = int(xp) + exp
                                        bot.duckinfo(username, b'xp', str(xp))
                                        irc.send(b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     you shot down the duck in ' + bytes(str(reacttime), 'utf-8') + b' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + bytes(str(exp), 'utf-8') + b' xp] [TOTAL DUCKS: ' + bytes(str(ducks), 'utf-8') + b']\x03\r\n')
                                    # has lucky charm
                                    if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                        lcxp = func.gettok(func.cnfread('duckhunt.cnf', 'lucky_charm', str(username)), 1, ',')
                                        exp = duckexp + int(lcxp)
                                        xp = int(xp) + int(exp)
                                        bot.duckinfo(username, b'xp', str(xp))
                                        irc.send(b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     you shot down the duck in ' + bytes(str(reacttime), 'utf-8') + b' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + bytes(str(exp), 'utf-8') + b' xp - Lucky Charm] [TOTAL DUCKS: ' + bytes(str(ducks), 'utf-8') + b']\x03\r\n')
                                    # reset duck info
                                    duck[duckid] = 'None'
                                    start_time = time.time()
                                    # silent rearm
                                    if gunconf == 'on':
                                        confiscatedguns = ''
                                    # no more ducks, reset fear
                                    if not duck_exists():
                                        fear_factor = False
                                    # searching the bushes
                                    thebushes = func.cnfread('duckhunt.cnf', 'rules', 'thebushes')
                                    if int(thebushes) > 0:
                                        searchbush = random.randrange(1, 100, 1)
                                        if int(searchbush) < int(thebushes):
                                            bushes = bot.searchthebushes(username)
                                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > ' + bytes(str(bushes), 'utf-8') + b'\r\n')
                                    # check for level up
                                    if int(xp) >= int(levelup):
                                        level_up(username)
                                    continue

                                # normal-gold ducks
                                if func.gettok(duckdata, 1, ',') == 'gold':
                                    # on first hit, they turn golden (the suck survived, golden duck detected
                                    ddmg = 1
                                    duckstat = random.randint(2, 3)
                                    # expl ammo
                                    if func.cnfexists('duckhunt.cnf', 'expl_ammo', str(username)):
                                        ddmg = 2
                                    duckdata = func.gettok(duckdata, 0, ',') + ',golden,' + str(duckstat)
                                    duck[duckid] = duckdata

                                    irc.send(b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     The duck surivived!     \x02\x034\\_O< [Life -' + str(ddmg).encode() + b']\x03\x02     \x02\x037* GOLDEN DUCK DETECTED *\x02\x03\r\n')
                                    continue

                                # golden ducks
                                if func.gettok(duckdata, 1, ',') == 'golden':

                                    duckhp = func.gettok(duckdata, 2, ',')

                                    # duck survived
                                    # expl ammo
                                    if func.cnfexists('duckhunt.cnf', 'expl_ammo', str(username)):
                                        if int(duckhp) > 2:
                                            ddmg = 2
                                            duckhp = int(duckhp) - int(ddmg)
                                            duckdata = func.gettok(duckdata, 0, ',') + ',' + func.gettok(duckdata, 1, ',') + ',' + str(duckhp)
                                            duck[duckid] = duckdata
                                            irc.send(b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     The GOLDEN DUCK surivived!     \x02\x034\\_O< [Life -' + str(ddmg).encode() + b']\x03\x02\r\n')
                                            continue
                                    # regular ammo
                                    if int(duckhp) > 1 and func.cnfexists('duckhunt.cnf', 'expl_ammo', str(username)) == False:
                                        ddmg = 1
                                        duckhp = int(duckhp) - int(ddmg)
                                        duckdata = func.gettok(duckdata, 0, ',') + ',' + func.gettok(duckdata, 1, ',') + ',' + str(duckhp)
                                        duck[duckid] = duckdata
                                        irc.send(b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     The GOLDEN DUCK surivived!     \x02\x034\\_O< [Life -' + str(ddmg).encode() + b']\x03\x02\r\n')
                                        continue

                                    # shot down the golden duck
                                    # expl ammo
                                    expl = False
                                    if func.cnfexists('duckhunt.cnf', 'expl_ammo', str(username)) and int(duckhp) <= 2:
                                        expl = True

                                    # regular ammo
                                    if int(duckhp) == 1 or expl == True:
                                        # top shot counter
                                        bot.tshotplus()
                                        if expl == True:
                                            expl = False
                                        # reaction time determination
                                        reacttime = round(time.time() - float(duck_time), 2)
                                        if best == '0':
                                            bot.duckinfo(username, b'best', str(reacttime))
                                        if float(best) > reacttime:
                                            bot.duckinfo(username, b'best', str(reacttime))
                                        # increase ducks
                                        gducks = int(gducks) + 1
                                        bot.duckinfo(username, b'gducks', str(gducks))
                                        # increase xp
                                        bot.data_check(username, 'lucky_charm')
                                        # does not have lucky charm
                                        if not func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                            exp = duckexp * 3
                                            xp = int(xp) + int(exp)
                                            bot.duckinfo(username, b'xp', str(xp))
                                            irc.send(b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     you shot down the GOLDEN DUCK in ' + bytes(str(reacttime), 'utf-8') + b' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + bytes(str(exp), 'utf-8') + b' xp] [TOTAL GOLDEN DUCKS: ' + bytes(str(gducks), 'utf-8') + b']\x03\r\n')
                                        # has lucky charm
                                        if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                            exp = duckexp * 3
                                            lcxp = func.gettok(func.cnfread('duckhunt.cnf', 'lucky_charm', str(username)), 1, ',')
                                            exp = int(exp) + int(lcxp)
                                            xp = int(xp) + int(exp)
                                            bot.duckinfo(username, b'xp', str(xp))
                                            irc.send(b"PRIVMSG " + duckchan + b" :" + username + b' > \x0314*BANG*\x03     you shot down the GOLDEN DUCK in ' + bytes(str(reacttime), 'utf-8') + b' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + bytes(str(exp), 'utf-8') + b' xp - Lucky Charm] [TOTAL GOLDEN DUCKS: ' + bytes(str(gducks), 'utf-8') + b']\x03\r\n')

                                        # searching the bushes
                                        searchbush = random.randrange(1, 100, 1)
                                        if int(searchbush) < int(thebushes):
                                            bushes = bot.searchthebushes(username)
                                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > ' + bytes(
                                                str(bushes), 'utf-8') + b'\r\n')

                                        # reset duck info
                                        duck[duckid] = 'None'
                                        start_time = time.time()
                                        # silent rearm
                                        if gunconf == 'on':
                                            confiscatedguns = ''
                                        # no more ducks, reset fear
                                        if not duck_exists():
                                            fear_factor = False
                                        # check for level up
                                        if int(xp) >= int(levelup):
                                            level_up(username)

                                        continue

                        # missed - no duck exists...
                        if not duck_exists():

                            accidents = int(accidents) + 1
                            bot.duckinfo(username, b'accidents', str(accidents))

                            # ricochet
                            ricochet = random.randint(1, 100)
                            if int(ricochet) < int(gunricochet) and int(gunricochet) > 0:
                                damage = ''
                                dmg = random.randint(1, 3)
                                if dmg == 1:
                                    damage = 'strikes a distant window!'
                                if dmg == 2:
                                    damage = 'strikes another hunter!'
                                if dmg == 3:
                                    damage = 'starts a wildfire!'

                                # determine xp subtract
                                rxp = dmg
                                if int(xp) >= 10000:
                                    rxp = dmg * 2
                                if int(xp) >= 5000 and int(xp) < 10000:
                                    rxp = dmg + 3
                                if int(xp) < 5000 and int(xp) >= 1500:
                                    rxp = dmg + 1

                                # gunconf is off
                                if gunconf == 'off':
                                    # deduct xp
                                    rxp = rxp + 4
                                    if int(xp) <= rxp:
                                        xp = 0
                                    if int(xp) > rxp:
                                        xp = int(xp) - rxp
                                    bot.duckinfo(username, str(xp))
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(str(damage), 'utf-8') + b' \x034[-' + str(dmg).encode() + b' xp] [Ricochet]\x03\r\n')
                                    continue

                                # determine accident insurance
                                bot.data_check(username, 'accident_insurance')
                                # has accident insurance
                                if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                    # deduct xp
                                    rxp = rxp + 4
                                    if int(xp) <= rxp:
                                        xp = 0
                                    if int(xp) > rxp:
                                        xp = int(xp) - rxp
                                    bot.duckinfo(username, b'xp', str(xp))
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(str(damage), 'utf-8') + b' \x034[-' + str(rxp).encode() + b' xp]\x03 \x033[GUN NOT CONFISCATED: Accident Insurance]\x03\r\n')
                                    continue
                                # does not have accident insurance
                                if not func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                    # deduct xp
                                    if int(xp) <= rxp:
                                        xp = 0
                                    if int(xp) > rxp:
                                        xp = int(xp) - rxp
                                    bot.duckinfo(username, b'xp', str(xp))
                                    # gun confiscation
                                    if confiscatedguns != '':
                                        confiscatedguns = str(confiscatedguns) + ',' + str(username)
                                    if confiscatedguns == '':
                                        confiscatedguns = str(username)

                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + bytes(str(damage), 'utf-8') + b' \x034[-' + str(rxp).encode() + b' xp] [GUN CONFISCATED: Ricochet]\x03\r\n')
                                    continue

                            # no ricochet
                            else:

                                damage = ''
                                dmg = random.randint(1, 3)
                                if dmg == 1:
                                    damage = 'Shot a distant window!'
                                if dmg == 2:
                                    damage = 'Shot another hunter!'
                                if dmg == 3:
                                    damage = 'Wildfire!'

                                # determine xp subtract
                                rxp = dmg
                                if int(xp) >= 10000:
                                    rxp = dmg * 2
                                if int(xp) >= 5000 and int(xp) < 10000:
                                    rxp = dmg + 3
                                if int(xp) < 5000 and int(xp) >= 1500:
                                    rxp = dmg + 1
                                if int(xp) < 1500:
                                    rxp = dmg
                                # gunconf is off
                                if gunconf == 'off':
                                    # deduct xp
                                    rxp = rxp + 4
                                    if int(xp) <= rxp:
                                        xp = 0
                                    if int(xp) > rxp:
                                        xp = int(xp) - rxp
                                    bot.duckinfo(username, b'xp', str(xp))
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03    What did you shoot at? There is no duck in the area...   \x034[-' + str(rxp).encode() + b' xp] [' + damage.encode() + b']\x03\r\n')
                                    continue
                                # determine accident insurance
                                bot.data_check(username, 'accident_insurance')
                                # has accident insurance
                                if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                    # deduct xp
                                    rxp = rxp + 4
                                    if int(xp) <= rxp:
                                        xp = 0
                                    if int(xp) > rxp:
                                        xp = int(xp) - rxp
                                    bot.duckinfo(username, b'xp', str(xp))
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03    What did you shoot at? There is no duck in the area...    \x034[-' + str(rxp).encode() + b' xp]\x03 \x033[GUN NOT CONFISCATED: Accident Insurance]\x03\r\n')
                                    continue
                                # does not have accident insurance
                                if not func.cnfexists('duckhunt.cnf', 'accident_insurance', str(username)):
                                    # deduct xp
                                    if int(xp) <= rxp:
                                        xp = 0
                                    if int(xp) > rxp:
                                        xp = int(xp) - rxp
                                    bot.duckinfo(username, b'xp', str(xp))
                                    # gun confiscation
                                    if confiscatedguns != '':
                                        confiscatedguns = str(confiscatedguns) + ',' + str(username)
                                    if confiscatedguns == '':
                                        confiscatedguns = str(username)
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*BANG*\x03    What did you shoot at? There is no duck in the area...   \x034[-' + str(rxp).encode() + b' xp] [GUN CONFISCATED: ' + damage.encode() + b']\x03\r\n')
                                    continue
# ======================================================================================================================
# !bread for reloading bread (v1.1.0 expansion) - !reloaf (secret command)
# ======================================================================================================================
                    if data[3].lower() == b':!reloaf' or data[3].lower() == b':!bread' or data3.lower() == b'!reloaf' or data3.lower() == b'!bread':
                        if bef == 'off':
                            continue
                        # new users with no stats, bread doesn't need to be reloaded
                        if func.cnfexists('duckhunt.cnf', 'ducks', str(username)) == False:
                            if infammo == 'on':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > Your bread doesn't need to be reloaded. | Bread Pieces: 12/12 | Loaf: \x02\x033Inf\x02\x03\r\n")
                            if infammo == 'off':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > Your bread doesn't need to be reloaded. | Bread Pieces: 12/12 | Loaf: 3/3\r\n")
                            continue

                        # reloading bread box
                        bread = func.gettok(bot.duckinfo(username, b'bread'), 0, '?')
                        mbread = func.gettok(bot.duckinfo(username, b'bread'), 1, '?')
                        loaf = func.gettok(bot.duckinfo(username, b'bread'), 2, '?')
                        mloaf = func.gettok(bot.duckinfo(username, b'bread'), 3, '?')

                        if int(bread) == 0:

                            # out of loaf
                            if int(loaf) == 0 and infammo == 'off':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x034You are out of bread loaves.\x03 | Bread Pieces:\x034 0\x03/' + bytes(str(mbread), 'utf-8') + b' | Loaf:\x034 0\x03/' + bytes(str(mloaf), 'utf-8') + b'\r\n')
                                continue

                            # successful reload
                            if infammo == 'off':
                                loaf = int(loaf) - 1

                            bread = mbread
                            breadbox = str(bread) + '?' + str(mbread) + '?' + str(loaf) + '?' + str(mloaf)
                            bot.duckinfo(username, b'bread', str(breadbox))
                            if infammo == 'on':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*Shmp..CLICK*\x03     You reload your bread box. | Bread Pieces: ' + bytes(str(bread), 'utf-8') + b'/' + bytes(str(mbread), 'utf-8') + b' | Loaf: \x02\x033Inf\x02\x03\r\n')
                            if infammo == 'off':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*Shmp..CLICK*\x03     You reload your bread box. | Bread Pieces: ' + bytes(str(bread), 'utf-8') + b'/' + bytes(str(mbread), 'utf-8') + b' | Loaf: ' + bytes(str(loaf), 'utf-8') + b'/' + bytes(str(mloaf), 'utf-8') + b'\r\n')
                            continue

                        if int(bread) > 0:
                            if infammo == 'on':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > your bread box doesn't need to be reloaded. | Bread Pieces: " + bytes(str(bread), 'utf-8') + b'/' + bytes(str(mbread), 'utf-8') + b' | Loaf: \x02\x033Inf\x02\x03\r\n')
                            if infammo == 'off':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > your bread box doesn't need to be reloaded. | Bread Pieces: " + bytes(str(bread), 'utf-8') + b'/' + bytes(str(mbread), 'utf-8') + b' | Loaf: ' + bytes(str(loaf), 'utf-8') + b'/' + bytes(str(mloaf), 'utf-8') + b'\r\n')
                            continue
# ======================================================================================================================
# !bef recode v1.1.0
# ======================================================================================================================
                    if data[3].lower() == b':!bef' or data3.lower() == b'!bef':
                        if bef == 'off':
                            continue
                        # new users with no stats
                        if not func.cnfexists('duckhunt.cnf', 'ducks', str(username)):
                            dinfo = '7?3?7?3,0,0,0,1,200,0,0,75?80?80,0,0,12?12?3?3,0'
                            func.cnfwrite('duckhunt.cnf', 'ducks', str(username), str(dinfo))
                            func.cnfwrite('duckhunt.cnf', 'ducks', 'cache', '1')

                        # player is bombed
                        if func.cnfexists('duckhunt.cnf', 'bombed', str(username)):
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x034Your clothes are crusty and filthy from being duck bombed. You cannot befriend ducks like this, you need new clothes.\r\n')
                            continue

                        # player is soggy
                        bot.data_check(username, 'soggy')
                        if func.cnfexists('duckhunt.cnf', 'soggy', str(username)):
                            # determine time remaining
                            # 1 hour timer calculation
                            timeleft = bot.data_check(str(username), 'soggy', 'get')
                            timemath = func.hour1() - math.ceil(time.time() - float(timeleft))
                            timemath = bot.timeconvertmsg(timemath)
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034Your clothes are all soggy. You cannot befriend ducks until you're dry. \x033[Time Remaining: " + bytes(str(timemath), 'utf-8') + b']\x03\r\n')
                            continue

                        # friending data
                        xp = bot.duckinfo(username, b'xp')
                        breadbox = bot.duckinfo(username, b'bread')
                        bread = func.gettok(breadbox, 0, '?')
                        mbread = func.gettok(breadbox, 1, '?')
                        loaf = func.gettok(breadbox, 2, '?')
                        mloaf = func.gettok(breadbox, 3, '?')
                        friend = bot.duckinfo(username, b'friend')
                        # inventory = bot.duckinfo(username, b'inv')
                        level = bot.duckinfo(username, b'level')
                        levelup = bot.duckinfo(username, b'levelup')
                        best = bot.duckinfo(username, b'best')

                        # Gun Lock for bread
                        if func.cnfexists('duckhunt.cnf', 'bread_lock', str(username)) and not duck_exists():
                            useleft = func.cnfread('duckhunt.cnf', 'bread_lock', str(username))
                            if int(useleft) == 1:
                                useleft = '0'
                                func.cnfdelete('duckhunt.cnf', 'bread_lock', str(username))
                            if int(useleft) > 1:
                                useleft = int(useleft) - 1
                                func.cnfwrite('duckhunt.cnf', 'bread_lock', str(username), str(useleft))
                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314*Bzzt..Click*\x03     \x034BREAD BOX LOCKED   [' + bytes(str(useleft), 'utf-8') + b']\x03\r\n')
                            continue

                        # out of bread
                        if int(bread) == 0:
                            if infammo == 'on':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x0314*BZZT*\x03     \x034EMPTY BOX\x03 | Bread pieces:\x034 0\x03/" + bytes(str(mbread), 'utf-8') + b" | Loaf: \x02\x033Inf\x02\x03   [\x02Reloaf\x02 your bread box.]\r\n")
                            if infammo == 'off':
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x0314*BZZT*\x03     \x034EMPTY BOX\x03 | Bread pieces:\x034 0\x03/" + bytes(str(mbread), 'utf-8') + b" | Loaf: " + bytes(str(loaf), 'utf-8') + b"/" + bytes(str(mloaf), 'utf-8') + b'   [\x02Reloaf\x02 your bread box.]\r\n')
                            continue

                        # tosses a peice of bread
                        bread = int(bread) - 1

                        # has popcorn
                        bot.data_check(str(username), 'popcorn')
                        if func.cnfexists('duckhunt.cnf', 'popcorn', str(username)):
                            popc = func.cnfread('duckhunt.cnf', 'popcorn', str(username))
                            if int(popc) > 0:
                                popc = int(popc) - 1
                                func.cnfwrite('duckhunt.cnf', 'popcorn', str(username), str(popc))

                        breadbox = str(bread) + '?' + str(mbread) + '?' + str(loaf) + '?' + str(mloaf)
                        bot.duckinfo(username, b'bread', str(breadbox))
                        # no duck in the area
                        if not duck_exists():
                            # deduct xp
                            rxp = random.randint(1, 2)
                            if int(xp) >= 10000 or int(level) >= 10:
                                rxp = rxp + random.randint(5,6)
                            elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                                rxp = rxp + random.randint(4,5)
                            elif int(xp) < 5000 and int(xp) >= 1500:
                                rxp = rxp + random.randint(2, 3)
                            # deduct xp
                            if int(xp) <= rxp:
                                xp = 0
                            if int(xp) > rxp:
                                xp = int(xp) - rxp
                            bot.duckinfo(username, b'xp', str(xp))

                            if func.cnfexists('duckhunt.cnf', 'popcorn', str(username).lower()) is True:
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Tosses a piece of popcorn at nothing? There are no ducks in the area. \x034[-1 Popcorn] [-' + bytes(str(rxp), 'utf-8') + b' xp]\x03\r\n')
                                continue
                            if not func.cnfexists('duckhunt.cnf', 'popcorn', str(username)):
                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > Tosses a piece of bread at nothing? There are no ducks in the area. \x034[-1 Bread] [-' + bytes(str(rxp), 'utf-8') + b' xp]\x03\r\n')
                                continue

                        # duck exists
                        if duck_exists():

                            # check if player is bedazzled
                            bot.data_check(username, 'bedazzled')
                            if func.cnfexists('duckhunt.cnf', 'bedazzled', str(username)):
                                rxp = random.randint(1, 2)
                                if int(xp) >= 10000 or int(level) >= 10:
                                    rxp = rxp * 6
                                elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                                    rxp = rxp * 4
                                elif int(xp) < 5000 and int(xp) >= 1500:
                                    rxp = rxp * 2

                                # deduct xp
                                if int(xp) <= rxp:
                                    xp = 0
                                if int(xp) > rxp:
                                    xp = int(xp) - rxp
                                bot.duckinfo(username, b'xp', str(xp))

                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034UNLUCKY\x03     You tossed in the wrong direction because you're bedazzled!     \x034[-" + bytes(str(rxp), 'utf-8') + b' xp] [Bedazzled]\r\n')
                                continue

                            # determine duck
                            duckdata = ''
                            duck_time = ''
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

                            # determine friend or not
                            friendornot = ''
                            # normal duck
                            if func.gettok(duckdata, 1, ',') == 'normal':
                                friendornot = random.randrange(1, 100, 1)
                            # normal-gold duck
                            if func.gettok(duckdata, 1, ',') == 'gold':
                                friendornot = random.randrange(0, 140, 1)
                            # golden duck
                            if func.gettok(duckdata, 1, ',') == 'golden':
                                friendornot = random.randrange(0, 110, 1)

                            # has popcorn
                            if func.cnfexists('duckhunt.cnf', 'popcorn', str(username)):
                                friendornot = int(friendornot) - 15
                            # unlucky
                            if friendornot > int(friendrate):
                                rxp = random.randint(1, 2)
                                if int(xp) >= 10000 or int(level) >= 10:
                                    rxp = rxp + random.randint(5, 6)
                                elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                                    rxp = rxp + random.randint(4, 5)
                                elif int(xp) < 5000 and int(xp) >= 1500:
                                    rxp = rxp + random.randint(2, 3)
                                if func.gettok(duckdata, 1, ',') == 'golden':
                                    rxp = int(rxp) + random.randint(1, 3)
                                # deduct xp
                                if int(xp) <= rxp:
                                    xp = 0
                                if int(xp) > rxp:
                                    xp = int(xp) - rxp
                                bot.duckinfo(username, b'xp', str(xp))

                                # normal duck
                                if func.gettok(duckdata, 1, ',') == 'normal':
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034UNLUCKY\x03     The duck didn't seem to notice. Try again.     \x02\\_O< QUACK\x02    \x034[-" + bytes(str(rxp), 'utf-8') + b' xp]\r\n')
                                    continue

                                # normal-gold
                                if func.gettok(duckdata, 1, ',') == 'gold':

                                    # first miss, not golden yet
                                    if func.numtok(duckdata, ',') == 2:
                                        duckdata = duckdata + ',1'
                                        duck[duckid] = duckdata
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034UNLUCKY\x03     The duck didn't seem to notice. Try again.     \x02\\_O< QUACK\x02    \x034[-" + bytes(str(rxp), 'utf-8') + b' xp]\r\n')
                                        continue

                                    # 2nd miss determine if duck will turn golden
                                    if int(func.gettok(duckdata, 2, ',')) >= 1:
                                        duckstat = random.randrange(3, 4, 1)
                                        duckdata = func.gettok(duckdata, 0, ',') + ',golden,' + str(duckstat)
                                        duck[duckid] = duckdata
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034UNLUCKY\x03     The duck didn't seem to notice. Try again.\x037    \x02\\_O<    * GOLDEN DUCK DETECTED *\x02\x03\r\n")
                                        continue

                                # golden
                                if func.gettok(duckdata, 1, ',') == 'golden':
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b" > \x034UNLUCKY\x03     The GOLDEN DUCK didn't seem to notice. Try again.     \x02\\_O< QUACK\x02    \x034[-" + bytes(str(rxp), 'utf-8') + b' xp]\r\n')
                                    continue

                            # friend
                            if friendornot <= int(friendrate):

                                # normal duck
                                if func.gettok(duckdata, 1, ',') == 'normal':

                                    # reaction time determination
                                    reacttime = round(time.time() - float(duck_time), 2)
                                    if best == '0':
                                        bot.duckinfo(username, b'best', str(reacttime))
                                    if float(best) > reacttime:
                                        bot.duckinfo(username, b'best', str(reacttime))

                                    # increase friends
                                    friend = int(friend) + 1
                                    bot.duckinfo(username, b'friend', str(friend))

                                    # increase xp
                                    bot.data_check(username, 'lucky_charm')

                                    # has lucky charm
                                    if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                        lcxp = func.gettok(func.cnfread('duckhunt.cnf', 'lucky_charm', str(username)), 1, ',')
                                        exp = duckexp + int(lcxp)
                                        xp = int(xp) + int(exp)
                                        bot.duckinfo(username, b'xp', str(xp))
                                        wooid = 'bread'
                                        if func.cnfexists('duckhunt.cnf', 'popcorn', str(username)):
                                            wooid = 'popcorn'
                                        wooid = wooid.encode()
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314FRIEND\x03     The duck ate the piece of ' + wooid + b'!     \x02\\_O< QUAACK!\x02\x033   [BEFRIENDED DUCKS: ' + bytes(str(friend), 'utf-8') + b'] [+' + bytes(str(exp), 'utf-8') + b' xp - Lucky Charm]\x03\r\n')

                                    # does not have lucky charm
                                    if not func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                        exp = duckexp
                                        xp = int(xp) + exp
                                        bot.duckinfo(username, b'xp', str(xp))
                                        wooid = 'bread'
                                        if func.cnfexists('duckhunt.cnf', 'popcorn', str(username)):
                                            wooid = 'popcorn'
                                        wooid = wooid.encode()
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314FRIEND\x03     The duck ate the piece of ' + wooid + b'!     \x02\\_O< QUAACK!\x02\x033   [BEFRIENDED DUCKS: ' + bytes(str(friend), 'utf-8') + b'] [+' + bytes(str(duckexp), 'utf-8') + b' xp]\x03\r\n')

                                    # reset duck info
                                    duck[duckid] = 'None'
                                    start_time = time.time()
                                    # silent rearm
                                    confiscatedguns = ''
                                    # searching the bushes
                                    thebushes = func.cnfread('duckhunt.cnf', 'rules', 'thebushes')
                                    if int(thebushes) > 0:
                                        searchbush = random.randrange(1, 100, 1)
                                        if int(searchbush) < int(thebushes):
                                            bushes = bot.searchthebushes(username)
                                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > ' + bytes(str(bushes), 'utf-8') + b'\r\n')
                                    # no more ducks, reset fear
                                    if not duck_exists():
                                        fear_factor = False
                                    # check for level up
                                    if int(xp) >= int(levelup):
                                        level_up(username)
                                    continue

                                # normal-gold duck
                                if func.gettok(duckdata, 1, ',') == 'gold':
                                    ddmg = 1
                                    woid = 'bread'
                                    if func.cnfexists('duckhunt.cnf', 'popcorn', str(username)):
                                        ddmg = 2
                                        woid = 'popcorn'
                                    duckstat = random.randint(2, 3)
                                    duckdata = func.gettok(duckdata, 0, ',') + ',golden,' + str(duckstat)
                                    duck[duckid] = duckdata
                                    irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314QUACK!!\x03     The duck ate the piece of ' + bytes(str(woid), 'utf8') + b' and kept flying! Try again.    \x034\x02\\_O< [ <3 +' + bytes(str(ddmg), 'utf-8') + b' ]\x02\x03     \x02\x037* GOLDEN DUCK DETECTED *\x02\x03\r\n')
                                    continue

                                # golden
                                if func.gettok(duckdata, 1, ',') == 'golden':
                                    duckhp = func.gettok(duckdata, 2, ',')

                                    # has popcorn
                                    if func.cnfexists('duckhunt.cnf', 'popcorn', str(username)):
                                        if int(duckhp) > 2:
                                            ddmg = 2
                                            duckhp = int(duckhp) - int(ddmg)
                                            duckdata = func.gettok(duckdata, 0, ',') + ',' + func.gettok(duckdata, 1, ',') + ',' + str(duckhp)
                                            duck[duckid] = duckdata
                                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314QUACK!!\x03     The GOLDEN DUCK ate the piece of popcorn and kept flying! Try again.     \x034\x02\\_O< [ <3 +' + bytes(str(ddmg), 'utf-8') + b' ]\x02\x03\r\n')
                                            continue
                                    # the duck kept flying
                                    if int(duckhp) > 1:
                                        ddmg = 1
                                        wid = 'bread'
                                        if func.cnfexists('duckhunt.cnf', 'popcorn', str(username)):
                                            ddmg = 2
                                            wid = 'popcorn'
                                        wid = wid.encode()
                                        duckhp = int(duckhp) - int(ddmg)
                                        duckdata = func.gettok(duckdata, 0, ',') + ',' + func.gettok(duckdata, 1, ',') + ',' + str(duckhp)
                                        duck[duckid] = duckdata
                                        irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314QUACK!!\x03     The GOLDEN DUCK ate the piece of ' + wid + b' and kept flying! Try again.     \x034\x02\\_O< [ <3 +' + bytes(str(ddmg), 'utf-8') + b' ]\x02\x03\r\n')
                                        continue

                                    # befriended the golden duck
                                    # popcorn
                                    popc = False
                                    if func.cnfexists('duckhunt.cnf', 'popcorn', str(username)) and int(duckhp) <= 2:
                                        popc = True

                                    if int(duckhp) == 1 or popc == True:
                                        woid = 'bread'
                                        if popc == True:
                                            woid = 'popcorn'
                                            popc = False
                                        # reaction time determination
                                        reacttime = round(time.time() - float(duck_time), 2)
                                        if best == '0':
                                            bot.duckinfo(username, b'best', str(reacttime))
                                        if float(best) > reacttime:
                                            bot.duckinfo(username, b'best', str(reacttime))
                                        # increase friends
                                        friend = int(friend) + 1
                                        bot.duckinfo(username, b'friend', str(friend))
                                        # increase xp
                                        bot.data_check(username, 'lucky_charm')

                                        # has lucky charm
                                        if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                            exp = duckexp * 3
                                            lcxp = func.gettok(func.cnfread('duckhunt.cnf', 'lucky_charm', str(username)), 1, ',')
                                            exp = int(exp) + int(lcxp)
                                            xp = int(xp) + int(exp)
                                            bot.duckinfo(username, b'xp', str(xp))
                                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314FRIEND\x03     The GOLDEN DUCK ate the piece of ' + bytes(str(woid), 'utf-8') + b'!     \x02\\_0< QUAACK!\x02\x033   [BEFRIENDED DUCKS: ' + bytes(str(friend), 'utf-8') + b'] [+' + bytes(str(exp), 'utf-8') + b' xp - Lucky Charm]\x03\r\n')

                                        # does not have lucky charm
                                        if not func.cnfexists('duckhunt.cnf', 'lucky_charm', str(username)):
                                            exp = duckexp * 3
                                            xp = int(xp) + int(exp)
                                            bot.duckinfo(username, b'xp', str(xp))
                                            irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > \x0314FRIEND\x03     The GOLDEN DUCK ate the piece of ' + bytes(str(woid), 'utf-8') + b'!     \x02\\_0< QUAACK!\x02\x033   [BEFRIENDED DUCKS: ' + bytes(str(friend), 'utf-8') + b'] [+' + bytes(str(exp), 'utf-8') + b' xp]\x03\r\n')

                                        # reset duck info
                                        duck[duckid] = 'None'
                                        start_time = time.time()
                                        # silent rearm
                                        confiscatedguns = ''
                                        # searching the bushes
                                        thebushes = func.cnfread('duckhunt.cnf', 'rules', 'thebushes')
                                        if int(thebushes) > 0:
                                            searchbush = random.randrange(1, 100, 1)
                                            if int(searchbush) < int(thebushes):
                                                bushes = bot.searchthebushes(username)
                                                irc.send(b'PRIVMSG ' + duckchan + b' :' + username + b' > ' + bytes(str(bushes), 'utf-8') + b'\r\n')
                                        # no more ducks, reset fear
                                        if not duck_exists():
                                            fear_factor = False
                                        # check for level up
                                        if int(xp) >= int(levelup):
                                            level_up(username)
                                        continue

                    # ======================================================================================================================
                    # !tshot - displays all the ducks shot
                    # ======================================================================================================================
                    if data[3].lower() == b':!tshot' or data3.lower() == b'!tshot':
                        daily = func.cnfread('duckhunt.cnf', 'top_shot', 'daily')
                        weekly = func.cnfread('duckhunt.cnf', 'top_shot', 'weekly')
                        monthly = func.cnfread('duckhunt.cnf', 'top_shot', 'monthly')
                        totalshot = func.cnfread('duckhunt.cnf', 'top_shot', 'totalshot')
                        msg = '\x034Today:\x03\x037 ' + str(daily) + '\x03 \x034This Week:\x03\x037 ' + str(weekly) + '\x03 \x034This Month:\x03\x037 ' + str(monthly) + '\x03 \x034Since Last Reset:\x03\x037 ' + str(totalshot)
                        irc.send(b'PRIVMSG ' + duckchan + b' :\x033[Super DuckHunt] ' + duckchan + b' Shot Ducks Statistics:\x03 ' + bytes(str(msg), 'utf-8') + b'\x03\r\n')
                        continue
                    # ======================================================================================================================
                    # !dshot - displays the daily ducks shot
                    # ======================================================================================================================
                    if data[3].lower() == b':!dshot' or data3.lower() == b'!dshot':
                        daily = func.cnfread('duckhunt.cnf', 'top_shot', 'daily')
                        irc.send(
                            b'PRIVMSG ' + duckchan + b' :\x033[Super DuckHunt] Daily Ducks Shot:\x03\x037 ' + bytes(
                                str(daily), 'utf-8') + b'\x03\r\n')
                        continue
                    # ======================================================================================================================
                    # !wshot - displays the weekly ducks shot
                    # ======================================================================================================================
                    if data[3].lower() == b':!wshot' or data3.lower() == b'!wshot':
                        weekly = func.cnfread('duckhunt.cnf', 'top_shot', 'weekly')
                        irc.send(
                            b'PRIVMSG ' + duckchan + b' :\x033[Super DuckHunt] Weekly Ducks Shot:\x03\x037 ' + bytes(
                                str(weekly), 'utf-8') + b'\x03\r\n')
                        continue
                    # ======================================================================================================================
                    # !mshot - displays the monthly ducks shot
                    # ======================================================================================================================
                    if data[3].lower() == b':!mshot' or data3.lower() == b'!mshot':
                        monthly = func.cnfread('duckhunt.cnf', 'top_shot', 'monthly')
                        irc.send(
                            b'PRIVMSG ' + duckchan + b' :\x033[Super DuckHunt] Monthly Ducks Shot:\x03\x037 ' + bytes(
                                str(monthly), 'utf-8') + b'\x03\r\n')
                        continue
                    # ======================================================================================================================
                    # !help
                    # ======================================================================================================================
                    if data[3].lower() == b':!help' or data[3].lower() == b':!about' or data[3].lower() == b':!commands' or data3.lower() == b'!help':
                        irc.send(b'PRIVMSG ' + duckchan + b' :For DuckHunt HELP: https://m0de-60.github.io/super-duckhunt-web/super-duckhunt-help.htm\r\n')
                        continue
                    # ======================================================================================================================
                    # !spawnduck <normal/golden> - Botmaster and Admin only
                    # <normal/golden> is optional, if using just !spawnduck a normal duck is spawned.
                    # ======================================================================================================================
                    if data[3].lower() == b':!spawnduck' or data3.lower() == b'!spawnduck':
                        if func.istok(botmaster, str(dusername), ',') == False and func.istok(adminlist, str(dusername),',') == False:
                            continue
                        if len(data) == 4 or datarelay is True:
                            for x in range(maxducks + 1):
                                if x == 0:
                                    continue
                                d_key = 'd' + str(x)
                                if duck[d_key] == 'None':
                                    spawnduck(d_key, 'normal')
                                    start_time = time.time()
                                    break
                                if x == maxducks:
                                    irc.send(b'NOTICE ' + username + b' :The maximum amount of ducks are currently spawned.\r\n')
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
