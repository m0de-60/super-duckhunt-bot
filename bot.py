#! /usr/bin/python3
# Mode60 https://m0de-60.github.io/web - SDH1.1.4 Final
# ABOUT INFO# ==========================================================================================================
# Title..........: Super DuckHunt v1.1.4 Python IRC Bot
# File...........: bot.py (bot script dependant functions)
# Python version.: v3.12.0 (does not work in older versions)
# Script version.: v1.1.4
# Language.......: English
# Description....: This is a function module used for Super DuckHunt.
# ======================================================================================================================
from configparser import RawConfigParser
from configparser import ConfigParser
import configparser
import re
import time
import random
# CURRENT FUNCTIONS LIST - SEE FUNCTION SECTION FOR DESCRIPTIONS =======================================================
# cnfcleanup
# data_check
# duckinfo
# iecheck
# inveffect
# isaccess
# isbotmaster
# resetdef
# resetshot
# searchthebushes
# shopprice
# timeconvertmsg
# tshotplus
# userdat
# ======================================================================================================================
# noinspection PySimplifyBooleanCheck

# debugging function
def debug(mode, data):
    if mode == '0':
        print('DEBUG: ' + str(data))
        return
    if mode != '0':
        print(str(mode) + ': ' + str(data))
        return

# FUNCTION #============================================================================================================
# Name...........: cnfcleanup
# Description....: routine maintenance procedure for duckhunt.cnf
# Syntax.........: cnfcleanup()
# Parameters.....: None
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def cnfcleanup():
    parser = RawConfigParser()
    parser.read('duckhunt.cnf')

    for name, value in parser.items('expl_ammo'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'expl_ammo', str(datkey))
            continue
    time.sleep(0.1)
    for name, value in parser.items('sabotage'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'sabotage', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('trigger_lock'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'trigger_lock', str(datkey))
            continue
    time.sleep(0.1)
    for name, value in parser.items('bread_lock'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'bread_lock', str(datkey))
            continue
    time.sleep(0.1)
    for name, value in parser.items('duck_jam'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'duck_jam', str(datkey))
            continue
    time.sleep(0.1)
    for name, value in parser.items('gun_grease'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'gun_grease', str(datkey))
            continue
        dat = cnfread('duckhunt.cnf', 'gun_grease', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if float(timem) >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'gun_grease', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('silencer'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'silencer', str(datkey))
            continue
        dat = cnfread('duckhunt.cnf', 'silencer', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'silencer', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('lucky_charm'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'lucky_charm', str(datkey))
            continue
        dat = gettok(cnfread('duckhunt.cnf', 'lucky_charm', str(datkey)), 0, ',')
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'lucky_charm', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('sunglasses'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'sunglasses', str(datkey))
            continue
        dat = cnfread('duckhunt.cnf', 'sunglasses', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'sunglasses', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('accident_insurance'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'accident_insurance', str(datkey))
            continue
        dat = cnfread('duckhunt.cnf', 'accident_insurance', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'accident_insurance', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('rain_coat'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'rain_coat', str(datkey))
            continue
        dat = cnfread('duckhunt.cnf', 'rain_coat', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'rain_coat', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('duck_bomb'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'duck_bomb', str(datkey))
            continue
        dat = gettok(cnfread('duckhunt.cnf', 'duck_bomb', str(datkey)), 0, ',')
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'duck_bomb', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('bedazzled'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'bedazzled', str(datkey))
            continue
        dat = cnfread('duckhunt.cnf', 'bedazzled', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(hour1()):
            cnfdelete('duckhunt.cnf', 'bedazzled', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('soggy'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'soggy', str(datkey))
            continue
        dat = cnfread('duckhunt.cnf', 'soggy', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'soggy', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('bombed'):
        datkey = '%s' % name
        if not cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            cnfdelete('duckhunt.cnf', 'bombed', str(datkey))
            continue
    time.sleep(0.1)
    return
# ===> cnfcleanup

# FUNCTION #============================================================================================================
# Name...........: data_check
# Description....: checks and handles items/effects time entries. This function also doubles as invetory/effects
#                  retreival for !duckstats, and used to determine if user has certain item in their inventory,
#                  replacing the use of b'inv' and b'effects' in duckinfo().
# Syntax.........: data_check(user, idtype, ext)
# Parameters.....: user - username to be checked
#                  idtype - Time entry idtype (see remarks)
#                  ext - optional extended data (see rmarks)
# Return values..: None specific, True for success and False for failure (in certain parameters)
# Author.........: Neo_Nemesis
# Modified.......:
# Remarks........: Acceptable types: gun_grease, trigger_lock, silencer, lucky_charm, sunglasses
#                                    lucky_charm, rain_coat, soggy, bedazzled (see example)
#                  Optional Extended data: 'add', 'del', 'get' (see example)
# Example........: data_check('username', 'gun_grease')
#                       --> this will check for an existing gun_grease timer and if time is spent, removes entry
#                  data_check('username', 'trigger_lock', 'add')
#                       --> this will add a trigger_lock time entry for username, existing entries are overwritten.
#                  data_check('username', 'silencer', 'del')
#                       --> this will remove a silencer time entry for username, if it exists.
#                       --> returns False is no entry exists
#                  data_check('username', 'lucky_charm', 'get')
#                       --> this will check to see if username has a lucky_charm entry, and returns the value.
#                       --> returns False is no entry exists
# ======================================================================================================================
def data_check(user, idtype, ext=''):
    if ext == 'add':
        cnfwrite('duckhunt.cnf', idtype, user, str(time.time()))
        return True
    elif ext == 'del':
        if cnfexists('duckhunt.cnf', idtype, user) is False:
            return False
        cnfdelete('duckhunt.cnf', idtype, user)
        return True
    elif ext == 'get':
        if cnfexists('duckhunt.cnf', idtype, user) is False:
            return False
        if cnfexists('duckhunt.cnf', idtype, user) is True:
            return cnfread('duckhunt.cnf', idtype, user)
        return False
    elif ext == '' and cnfexists('duckhunt.cnf', idtype, user):
        timem = cnfread('duckhunt.cnf', idtype, user)
        # update 1.1.0 - for lucky charm and expansion and duck bomb recode
        if numtok(str(timem), ',') > 1:
            timem = gettok(str(timem), 0, ',')
        # # # ===
        timem = time.time() - float(timem)
        if idtype == 'gun_grease':
            if timem >= float(hour24()):
                cnfdelete('duckhunt.cnf', 'gun_grease', user)
                return
        # update 1.1.0 - removed 24 hour parameter for Gun Lock
        # if idtype == 'trigger_lock':
        #     if timem >= float(hour24()):
        #         cnfdelete('duckhunt.cnf', 'trigger_lock', user)
        #         return
        if idtype == 'silencer':
            if timem >= float(hour24()):
                cnfdelete('duckhunt.cnf', 'silencer', user)
                return
        # update 1.1.0 - lucky charm change, now stored in token string " time,lcxp "
        if idtype == 'lucky_charm':
            if timem >= float(hour24()):
                cnfdelete('duckhunt.cnf', 'lucky_charm', user)
                return
        if idtype == 'sunglasses':
            if timem >= float(hour24()):
                cnfdelete('duckhunt.cnf', 'sunglasses', user)
                return
        if idtype == 'accident_insurance':
            if timem >= float(hour24()):
                cnfdelete('duckhunt.cnf', 'accident_insurance', user)
                return
        if idtype == 'rain_coat':
            if timem >= float(hour24()):
                cnfdelete('duckhunt.cnf', 'rain_coat', user)
                return
        # update v1.1.0 - restructured duck bomb code for !bomb recode
        if idtype == 'duck_bomb':
            bombent = gettok(cnfread('duckhunt.cnf', 'duck_bomb', user), 1, ',')
            if int(bombent) == 0 and timem >= float(hour24()):
                cnfdelete('duckhunt.cnf', 'duck_bomb', user)
                return
            if int(bombent) > 0 and timem >= float(hour24()):
                cnfwrite('duckhunt.cnf', 'duck_bomb', user, str(time.time()) + ',0')
                return
        if idtype == 'bedazzled':
            if timem >= float(hour1()):
                cnfdelete('duckhunt.cnf', 'bedazzled', user)
                return
        if idtype == 'soggy':
            if timem >= float(hour1()):
                cnfdelete('duckhunt.cnf', 'soggy', user)
                return
        # explosive ammo, update 1.1.0
        if idtype == 'expl_ammo':
            if cnfexists('duckhunt.cnf', 'expl_ammo', str(user)):
                uself = cnfread('duckhunt.cnf', 'expl_ammo', str(user))
                if int(uself) == 0:
                    cnfdelete('duckhunt.cnf', 'expl_ammo', str(user))
                    return
        # popcorn ammo, update 1.1.0
        if idtype == 'popcorn':
            if cnfexists('duckhunt.cnf', 'popcorn', str(user)):
                popl = cnfread('duckhunt.cnf', 'popcorn', str(user))
                if int(popl) == 0:
                    cnfdelete('duckhunt.cnf', 'popcorn', str(user))
                    return
# ===> data_check

# FUNCTION #============================================================================================================
# Name...........: duckinfo
# Description....: Returns or changes specified user Duck stats
# Syntax.........: duckinfo(user, req, data)
# Parameters.....: user - username
#                  req - info to be retreived
#                  data - optional, new data to be written
# Return values..: Returns specified duck stats
#                  Successful data write - 1
#                  Error/unkown command - -1
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def duckinfo(user, req, data=''):
    cnfdat = cnfread('duckhunt.cnf', 'ducks', str(user))
    if req == b'ammo':
        if data == '':
            return gettok(cnfdat, 0, ',')
        else:
            duck_info = reptok(cnfdat, 0, ',', data)
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'ducks':
        if data == '':
            return gettok(cnfdat, 1, ',')
        else:
            duck_info = reptok(cnfdat, 1, ',', str(data))
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'gducks':
        if data == '':
            return gettok(cnfdat, 2, ',')
        else:
            duck_info = reptok(cnfdat, 2, ',', data)
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'xp':
        if data == '':
            return gettok(cnfdat, 3, ',')
        else:
            duck_info = reptok(cnfdat, 3, ',', str(data))
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'level':
        if data == '':
            return gettok(cnfdat, 4, ',')
        else:
            duck_info = reptok(cnfdat, 4, ',', data)
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'levelup':
        if data == '':
            return gettok(cnfdat, 5, ',')
        else:
            duck_info = reptok(cnfdat, 5, ',', data)
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'effects':
        if data == '':
            return gettok(cnfdat, 6, ',')
        else:
            duck_info = reptok(cnfdat, 6, ',', data)
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'inv':
        if data == '':
            return gettok(cnfdat, 7, ',')
        else:
            duck_info = reptok(cnfdat, 7, ',', data)
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'guninfo':
        if data == '':
            return gettok(cnfdat, 8, ',')
        else:
            duck_info = reptok(cnfdat, 8, ',', data)
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'best':
        if data == '':
            return gettok(cnfdat, 9, ',')
        else:
            duck_info = reptok(cnfdat, 9, ',', data)
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'accidents':
        if data == '':
            return gettok(cnfdat, 10, ',')
        else:
            duck_info = reptok(cnfdat, 10, ',', data)
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'bread':
        if data == '':
            return gettok(cnfdat, 11, ',')
        else:
            duck_info = reptok(cnfdat, 11, ',', data)
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'friend':
        if data == '':
            return gettok(cnfdat, 12, ',')
        else:
            duck_info = reptok(cnfdat, 12, ',', data)
            cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    return -1
# ===> duckinfo

# FUNCTION #============================================================================================================
# Name...........: iecheck
# Description....: Checks all items/effect time entries and removes any that time result is over the limit
# Syntax.........: iecheck(user)
# Parameters.....: user - username to be checked
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def iecheck(user):
    if cnfexists('duckhunt.cnf', 'ducks', str(user)) is False:
        return
# gun grease check =====================================================================================================
    if cnfexists('duckhunt.cnf', 'gun_grease', user) is True:
        timem = cnfread('duckhunt.cnf', 'gun_grease', user)
        timem = time.time() - float(timem)
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'gun_grease', user)
# Gun Lock check ===================================================================================================
# update 1.1.0 - removed 24 hour parameter and replaced with different parameters
#    if cnfexists('duckhunt.cnf', 'trigger_lock', user) is True:
#        timem = cnfread('duckhunt.cnf', 'trigger_lock', user)
#        timem = time.time() - float(timem)
#        if timem >= float(hour24()):
#            cnfdelete('duckhunt.cnf', 'trigger_lock', user)
# silencer check =======================================================================================================
    if cnfexists('duckhunt.cnf', 'silencer', user) is True:
        timem = cnfread('duckhunt.cnf', 'silencer', user)
        timem = time.time() - float(timem)
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'silencer', user)
# lucky charm check ====================================================================================================
    # update 1.1.0 - lucky charm now stored as token string " time,lcxp "
    if cnfexists('duckhunt.cnf', 'lucky_charm', user) is True:
        timem = gettok(cnfread('duckhunt.cnf', 'lucky_charm', user), 0, ',')
        timem = time.time() - float(timem)
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'lucky_charm', user)
# sunglasses check =====================================================================================================
    if cnfexists('duckhunt.cnf', 'sunglasses', user) is True:
        timem = cnfread('duckhunt.cnf', 'sunglasses', user)
        timem = time.time() - float(timem)
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'sunglasses', user)
# accident insurance check =============================================================================================
    if cnfexists('duckhunt.cnf', 'accident_insurance', user) is True:
        timem = cnfread('duckhunt.cnf', 'accident_insurance', user)
        timem = time.time() - float(timem)
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'accident_insurance', user)
# rain coat check ======================================================================================================
    if cnfexists('duckhunt.cnf', 'rain_coat', user) is True:
        timem = cnfread('duckhunt.cnf', 'rain_coat', user)
        timem = time.time() - float(timem)
        if timem >= float(hour24()):
            cnfdelete('duckhunt.cnf', 'rain_coat', user)
# duck bomb check ======================================================================================================
    # update 1.1.0 restructured duck bomb for !bomb recode ENTRY: b'username' = time,X
    #                                                             X = bomb uses, if X = 0 then no bombs for 24 hrs
    if cnfexists('duckhunt.cnf', 'duck_bomb', user) is True:
        bombent = gettok(cnfread('duckhunt.cnf', 'duck_bomb', user), 1, ',')
        if int(bombent) == 0:
            timem = gettok(cnfread('duckhunt.cnf', 'duck_bomb', user), 0, ',')
            timem = time.time() - float(timem)
            if timem >= float(hour24()):
                cnfdelete('duckhunt.cnf', 'duck_bomb', user)
        if int(bombent) > 0:
            timem = gettok(cnfread('duckhunt.cnf', 'duck_bomb', user), 0, ',')
            timem = time.time() - float(timem)
            if timem >= float(hour24()):
                cnfwrite('duckhunt.cnf', 'duck_bomb', user, str(time.time()) + ',0')
# soggy check ==========================================================================================================
    if cnfexists('duckhunt.cnf', 'soggy', user) is True:
        timem = cnfread('duckhunt.cnf', 'soggy', user)
        timem = time.time() - float(timem)
        if timem >= float(hour1()):
            cnfdelete('duckhunt.cnf', 'soggy', user)
# bedazzled check ======================================================================================================
    if cnfexists('duckhunt.cnf', 'bedazzled', user) is True:
        timem = cnfread('duckhunt.cnf', 'bedazzled', user)
        timem = time.time() - float(timem)
        if timem >= float(hour1()):
            cnfdelete('duckhunt.cnf', 'bedazzled', user)
# expl ammo check ======================================================================================================
    # update 1.1.0
    if cnfexists('duckhunt.cnf', 'expl_ammo', user) is True:
        expl = cnfread('duckhunt.cnf', 'expl_ammo', user)
        if int(expl) == 0:
            cnfdelete('duckhunt.cnf', 'expl_ammo', user)
# popcorn check ========================================================================================================
    # update 1.1.0
    if cnfexists('duckhunt.cnf', 'popcorn', user) is True:
        pop = cnfread('duckhunt.cnf', 'popcorn', user)
        if int(pop) == 0:
            cnfdelete('duckhunt.cnf', 'popcorn', user)
# ===> iecheck

# FUNCTION #============================================================================================================
# Name...........: inveffect
# Description....: Returns a formatted string for use in !duckstats for inventory and effects display
# Syntax.........: inveffect(user)
# Parameters.....: user - username to be formatted
# Return values..: Returns a formatted string
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def inveffect(user):
    huntingbag = '0'
    effects = '0'
    # gun grease
    data_check(str(user), 'gun_grease')
    if cnfexists('duckhunt.cnf', 'gun_grease', str(user)) is True:
        huntingbag = '\x037,1Gun Grease'
    # gun lock
    if cnfexists('duckhunt.cnf', 'trigger_lock', str(user)) is True:
        invuse = cnfread('duckhunt.cnf', 'trigger_lock', str(user))
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Gun Lock \x034,1[' + str(invuse) + ']'
        if huntingbag == '0':
            huntingbag = '\x037,1Gun Lock\x034,1 [' + str(invuse) + ']'
    # silencer
    data_check(str(user), 'silencer')
    if cnfexists('duckhunt.cnf', 'silencer', str(user)) is True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Silencer'
        if huntingbag == '0':
            huntingbag = '\x037,1Silencer'
    # lucky charm
    data_check(str(user), 'lucky_charm')
    if cnfexists('duckhunt.cnf', 'lucky_charm', str(user)) is True:
        invuse = gettok(cnfread('duckhunt.cnf', 'lucky_charm', str(user)), 1, ',')
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 Lucky Charm \x034,1[+' + str(invuse) + 'xp]'
        if huntingbag == '0':
            huntingbag = '\x037,1Lucky Charm \x034,1[+' + str(invuse) + 'xp]'
    # sunglasses
    data_check(str(user), 'sunglasses')
    if cnfexists('duckhunt.cnf', 'sunglasses', str(user)) is True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Sunglasses'
        if huntingbag == '0':
            huntingbag = '\x037,1Sunglasses'
    # accident insurance
    data_check(str(user), 'accident_insurance')
    if cnfexists('duckhunt.cnf', 'accident_insurance', str(user)) is True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Accident Insurance'
        if huntingbag == '0':
            huntingbag = '\x037,1Accident Insurance'
    # rain coat
    data_check(str(user), 'rain_coat')
    if cnfexists('duckhunt.cnf', 'rain_coat', str(user)) is True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Rain Coat'
        if huntingbag == '0':
            huntingbag = '\x037,1Rain Coat'
    # v.1.1.0 for bread expansion
    if cnfexists('duckhunt.cnf', 'bread_lock', str(user)) is True:
        invuse = cnfread('duckhunt.cnf', 'bread_lock', str(user))
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 Bread Box Lock \x034,1[' + str(invuse) + ']'
        if huntingbag == '0':
            huntingbag = '\x037,1Bread Box Lock \x034,1[' + str(invuse) + ']'
    # v.1.1.0 expl ammo
    data_check(str(user), 'expl_ammo')
    if cnfexists('duckhunt.cnf', 'expl_ammo', str(user)) is True:
        expl = cnfread('duckhunt.cnf', 'expl_ammo', str(user))
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 Explosive Ammo \x034,1[' + str(expl) + ']'
        if huntingbag == '0':
            huntingbag = '\x037,1Explosive Ammo \x034,1[' + str(expl) + ']'
    # v.1.1.0 bag of popcorn
    data_check(str(user), 'popcorn')
    if cnfexists('duckhunt.cnf', 'popcorn', str(user)) is True:
        pop = cnfread('duckhunt.cnf', 'popcorn', str(user))
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 Bag of Popcorn \x034,1[' + str(pop) + ']'
        if huntingbag == '0':
            huntingbag = '\x037,1Bag of Popcorn \x034,1[' + str(pop) + ']'
    # assemble hunting bag
    if huntingbag != '0':
        huntingbag = '\x030,1[HUNTING BAG] ' + huntingbag
    if huntingbag == '0':
        huntingbag = '\x030,1[HUNTING BAG]\x034,1 None'
    # bedazzled
    data_check(str(user), 'bedazzled')
    if cnfexists('duckhunt.cnf', 'bedazzled', str(user)) is True:
        if effects != '0':
            effects = effects + ' \x030,1|\x037,1 ' + 'Bedazzled'
        if effects == '0':
            effects = '\x037,1Bedazzled'
    # soggy
    data_check(str(user), 'soggy')
    if cnfexists('duckhunt.cnf', 'soggy', str(user)) is True:
        if effects != '0':
            effects = effects + ' \x030,1|\x037,1 ' + 'Soggy'
        if effects == '0':
            effects = '\x037,1Soggy'
    # sabotaged
    if cnfexists('duckhunt.cnf', 'sabotage', str(user)) is True:
        if effects != '0':
            effects = effects + ' \x030,1|\x037,1 ' + 'Sabotage'
        if effects == '0':
            effects = '\x037,1Sabotage'
    # bombed
    if cnfexists('duckhunt.cnf', 'bombed', str(user)) is True:
        if effects != '0':
            effects = effects + ' \x030,1|\x037,1 Duck Bombed'
        if effects == '0':
            effects = '\x037,1Duck Bombed'
    # assemble effects box
    if effects != '0':
        effects = '\x030,1[EFFECTS] ' + effects
    if effects == '0':
        effects = '\x030,1[EFFECTS]\x034,1 None'
    # return formatted message
    return huntingbag + '::' + effects
# ===> inveffect

# FUNCTION #============================================================================================================
# Name...........: isaccess
# Description....: checks if user has bot access to botmaster and/or admin
# Syntax.........: isaccess(user)
# Parameters.....: user - username to be checked
# Return values..: Returns True - user exists in botmaster or admin list
#                  Returns False - user does not exist in botmaster or admin list
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def isaccess(user):
    # print(user)
    admin = cnfread('duckhunt.cnf', 'duckhunt', 'admin')
    # print(admin)
    botmaster = cnfread('duckhunt.cnf', 'duckhunt', 'botmaster')
    # print(botmaster)
    if istok(str(admin), str(user), ',') is True:
        return True
    if istok(str(botmaster), str(user), ',') is True:
        return True
    return False
# ===> isaccess

# FUNCTION #============================================================================================================
# Name...........: resetdef
# Description....: Restores duckhunt.cnf to pre-configured original settings
# Syntax.........: resetdef()
# Parameters.....: None
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def resetdef():
    cnfwrite('duckhunt.cnf', 'duckhunt', 'maxducks', '6')
    global maxducks
    maxducks = 6

    cnfwrite('duckhunt.cnf', 'duckhunt', 'spawntime', '1800')
    global spawntime
    spawntime = 1800

    cnfwrite('duckhunt.cnf', 'duckhunt', 'flytime', '1500')
    global flytime
    flytime = 1500

    cnfwrite('duckhunt.cnf', 'duckhunt', 'duckexp', '15')
    global duckexp
    duckexp = 15

    cnfwrite('duckhunt.cnf', 'duckhunt', 'duckfear', '45')
    global duckfear
    duckfear = 45

    cnfwrite('duckhunt.cnf', 'duckhunt', 'duckgold', '40')
    global duckgold
    duckgold = 40

    cnfwrite('duckhunt.cnf', 'duckhunt', 'friendrate', '70')
    global friendrate
    friendrate = 71

    cnfwrite('duckhunt.cnf', 'duckhunt', 'floodcheck', '10,8')
    global flood_check
    flood_check = True

    cnfwrite('duckhunt.cnf', 'rules', 'gunricochet', '5')
    global gunricochet
    gunricochet = 5

    cnfwrite('duckhunt.cnf', 'rules', 'thebushes', '15')
    global thebushes
    thebushes = 15

    cnfwrite('duckhunt.cnf', 'rules', 'gunconf', 'on')
    global gunconf
    gunconf = 'on'

    cnfwrite('duckhunt.cnf', 'rules', 'infammo', 'off')
    global infammo
    infammo = 'off'

    cnfwrite('duckhunt.cnf', 'rules', 'bang', 'on')
    global bang
    bang = 'on'

    cnfwrite('duckhunt.cnf', 'rules', 'bef', 'on')
    global bef
    bef = 'on'

    cnfwrite('duckhunt.cnf', 'duckhunt', 'maint', '24')
    global maint
    maint = '24'

    cnfwrite('duckhunt.cnf', 'duckhunt', 'maint_time', str(time.time()))
    global maint_time
    maint_time = str(time.time())

    time.sleep(0.10)

    parser = RawConfigParser()
    parser.read('duckhunt.cnf')

    for name, value in parser.items('flood_protection'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'flood_protection', str(datkey))
        continue

    time.sleep(0.10)

    cnfwrite('duckhunt.cnf', 'flood_protection', '!bang', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!duckstats', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!shop', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!bef', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!reload', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!bomb', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!tshot', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!mshot', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!help', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!swim', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!wshot', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!dshot', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!about', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!topduck', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!reloaf', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '!bread', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '\x01version\x01', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '\x01finger\x01', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', '\x01ping', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', 'version', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', 'finger', 'True')
    cnfwrite('duckhunt.cnf', 'flood_protection', 'ping', 'True')

    time.sleep(0.10)

    resetshot()

    time.sleep(0.10)

    statreset()

    return
# ===> resetdef

# FUNCTION #============================================================================================================
# Name...........: resetshot
# Description....: Resets total shot counter data
# Syntax.........: resetshot()
# Parameters.....: None
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def resetshot():
    cnfwrite('duckhunt.cnf', 'top_shot', 'daily', '0')
    global daily
    daily = '0'

    cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', '0')
    global weekly
    weekly = '0'

    cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', '0')
    global monthly
    monthly = '0'

    cnfwrite('duckhunt.cnf', 'top_shot', 'totalshot', '0')
    global totalshot
    totalshot = '0'

    cnfwrite('duckhunt.cnf', 'top_shot', 't_day', '1')
    cnfwrite('duckhunt.cnf', 'top_shot', 't_week', '1')
    cnfwrite('duckhunt.cnf', 'top_shot', 't_month', '1')
    return
# ===> resetshot

# FUNCTION #============================================================================================================
# Name...........: searchthebushes
# Description....: Function control for searching the bushes
# Syntax.........: searchthebushes(user)
# Parameters.....: user = username of player who is searching
# Return values..: returns a formatted message for searching theb ushes
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def searchthebushes(user):
    srchtxt = 'By searching the bushes around the duck, you find'
    ammo = duckinfo(user, b'ammo')
    global bang
    bang = cnfread('duckhunt.cnf', 'rules', 'bang')
    global bef
    bef = cnfread('duckhunt.cnf', 'rules', 'bef')

    rounds = gettok(ammo, 0, '?')
    mrounds = gettok(ammo, 2, '?')
    mags = gettok(ammo, 1, '?')
    mmags = gettok(ammo, 3, '?')

    xp = duckinfo(str(user), b'xp')

    srch = random.randint(1, 11)
    if int(srch) == 1 or int(srch) == 3 or int(srch) == 5 or int(srch) == 6 or int(srch) == 7 or int(srch) == 8 or int(srch) == 11:
        srch = random.randrange(1, 11, 1)
    if int(srch) == 1:
        return str(srchtxt) + ' a broken Lucky Charm. \x033Better luck next time.\x03'

    if int(srch) == 2:
        return str(srchtxt) + ' a fishing weight. \x033Better luck next time.\x03'

    if int(srch) == 3:
        xp = int(xp) + 50
        duckinfo(str(user), b'xp', str(xp))
        return str(srchtxt) + ' a duck booklet. \x033[+50 xp]\x03'

    if int(srch) == 4:
        xp = int(xp) + 5
        duckinfo(str(user), b'xp', str(xp))
        return str(srchtxt) + ' a duck feather. \x033[+5 xp]\x03'

    if int(srch) == 5:
        if int(rounds) == int(mrounds) or bang == 'off':
            return str(srchtxt) + ' a rusty fishing lure. \x033Better luck next time.\x03'

        if int(rounds) < int(mrounds):
            rounds = int(rounds) + 1
            ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
            duckinfo(user, b'ammo', ammo)
            return str(srchtxt) + ' an extra bullet. \x033[Rounds: ' + str(rounds) + '/' + str(mrounds) + ' | Magazines: ' + str(mags) + '/' + str(mmags) + '\x03'

    if int(srch) == 6:
        data_check(str(user), 'lucky_charm')
        if cnfexists('duckhunt.cnf', 'lucky_charm', str(user)):
            xp = int(xp) + 5
            duckinfo(str(user), b'xp', str(xp))
            return str(srchtxt) + ' a duck feather. \x033[+5 xp]\x03'

        if not cnfexists('duckhunt.cnf', 'lucky_charm', str(user)):
            # found = 'Lucky Charm'
            lcxp = random.randint(3, 8)
            cnfwrite('duckhunt.cnf', 'lucky_charm', str(user), str(time.time()) + ',' + str(lcxp))
            return str(srchtxt) + ' a Lucky Charm. \x033You will earn an extra ' + str(lcxp) + ' xp for every duck for 24 hrs.\x03'

    if int(srch) == 7:
        # found = 'Golden Duck Feather'
        xp = int(xp) + 150
        duckinfo(str(user), b'xp', str(xp))
        return str(srchtxt) + ' a golden duck feather. \x033[+150 xp]\x03'

    if int(srch) == 8:
        # found = 'Frog'
        xp = int(xp) + 25
        duckinfo(str(user), b'xp', str(xp))
        return str(srchtxt) + ' a frog.    * RIBBIT * \x033[+25 xp]\x03'

    if int(srch) == 9:
        # found = 'Sunglasses'
        cnfwrite('duckhunt.cnf', 'sunglasses', str(user), str(time.time()))
        return str(srchtxt) + ' a pair of Sunglasses. \x033You are now protected from bedazzlement for 24 hours.\x03'

    # future secrets: this second frog will eventually become a fishing pole. Trout master?
    if int(srch) == 10:
        xp = int(xp) + 25
        duckinfo(str(user), b'xp', str(xp))
        return str(srchtxt) + ' a frog.    * RIBBIT * \x033[+25 xp]\x03'

    if int(srch) == 11:
        xp = int(xp) + 175
        duckinfo(str(user), b'xp', str(xp))
        return str(srchtxt) + ' a duck enthusiast booklet. \x033[+175 xp]\x03'
# ===> searchthebushes

# FUNCTION #============================================================================================================
# Name...........: shopprice
# Description....: Determines price of specified item. CHANGE YOUR PRICE VALUES HERE
#                  Item prices vary based on user stats, for !shop
# Syntax.........: shopprice(user, itemid)
# Parameters.....: user - name of user who is using !shop
#                  itemid - !shop ID of the item.
# Return values..: Returns the specified price of the item
#                  Returns 0 if unknown/invalid itemid specified
# Author.........: Neo_Nemesis
# Remarks........: Update 1.1.0, shop remodel - moved some items, created new items
#                  more cost handling based on player stats
# Modified.......:
# ======================================================================================================================
def shopprice(user, itemid):
    # data prep
    ammo = duckinfo(user, b'ammo')
    mrounds = gettok(ammo, 2, '?')
    mmags = gettok(ammo, 3, '?')
    guninfo = duckinfo(user, b'guninfo')
    accuracy = gettok(guninfo, 0, '?')
    mreliability = gettok(guninfo, 2, '?')
    # Extra Bullet
    if int(itemid) == 1:
        return 7
    # Refill Magazine
    if int(itemid) == 2:
        if int(mrounds) == 7:
            return 20
        if int(mrounds) == 8:
            return 25
        if int(mrounds) == 9:
            return 30
        if int(mrounds) == 10:
            return 35
        if int(mrounds) >= 11:
            return 40
    # gun cleaning
    if int(itemid) == 3:
        if int(mreliability) <= 80:
            return 30
        if 80 < int(mreliability) < 85:
            return 35
        if 85 <= int(mreliability) < 90:
            return 40
        if 90 <= int(mreliability) < 95:
            return 45
        if 95 <= int(mreliability) <= 100:
            return 50
    # explosive ammo
    if int(itemid) == 4:
        return 35
    # return confiscated gun
    if int(itemid) == 5:
        return 30
    # gun grease
    if int(itemid) == 6:
        return 15
    # gun uprade
    if int(itemid) == 7:
        if 90 < int(accuracy) < 100 <= int(mreliability):
            return 350
        elif int(accuracy) <= 75 and int(mreliability) <= 80:
            return 200
        elif int(accuracy) > 75 and int(mreliability) > 80:
            return 300
        else:
            return 250
    # Gun Lock
    if int(itemid) == 8:
        if int(mrounds) == 7:
            return 25
        if int(mrounds) == 8:
            return 30
        if int(mrounds) == 9:
            return 35
        if int(mrounds) == 10:
            return 40
        if int(mrounds) == 11:
            return 45
        if int(mrounds) >= 12:
            return 50
    # silencer
    if int(itemid) == 9:
        return 20
    # lucky charm
    if int(itemid) == 10:
        return 30
    # sunglasses
    if int(itemid) == 11:
        return 20
    # dry clothes
    if int(itemid) == 12:
        if cnfexists('duckhunt.cnf', 'soggy', str(user.lower())) is False and cnfexists('duckhunt.cnf', 'bombed', str(user.lower())) is False:
            return 25
        if cnfexists('duckhunt.cnf', 'soggy', str(user.lower())) is True and cnfexists('duckhunt.cnf', 'bombed', str(user.lower())) is False:
            return 25
        if cnfexists('duckhunt.cnf', 'soggy', str(user.lower())) is False and cnfexists('duckhunt.cnf', 'bombed', str(user.lower())) is True:
            return 50
        if cnfexists('duckhunt.cnf', 'soggy', str(user.lower())) is True and cnfexists('duckhunt.cnf', 'bombed', str(user.lower())) is True:
            return 75
    # eye drops
    if int(itemid) == 13:
        return 35
    # mirror
    if int(itemid) == 14:
        return 35
    # handful of sand
    if int(itemid) == 15:
        return 15
    # water bucket
    if int(itemid) == 16:
        return 20
    # sabotage
    if int(itemid) == 17:
        return 15
    # accident insurance
    if int(itemid) == 18:
        return 25
    # loaf of bread
    if int(itemid) == 19:
        return 30
    # bag of popcorn
    if int(itemid) == 20:
        return 40
    # bread box lock
    if int(itemid) == 21:
        return 35
    # rain coat
    if int(itemid) == 22:
        return 30
    # magazine upgrade
    if int(itemid) == 23:
        if int(mrounds) == 7:
            return 40
        if int(mrounds) == 8:
            return 45
        if int(mrounds) == 9:
            return 50
        if int(mrounds) == 10:
            return 55
        if int(mrounds) >= 11:
            return 60
    # additional magazine
    if int(itemid) == 24:
        if int(mmags) == 3:
            return 75
        if int(mmags) >= 4:
            return 100
    # unkown item/ID
    return 0
# ===> shopprice

# FUNCTION #============================================================================================================
# Name...........: statreset
# Description....: Clears player stats and all player entries
# Syntax.........: statreset()
# Parameters.....: None
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def statreset():
    parser = RawConfigParser()
    parser.read('duckhunt.cnf')

    for name, value in parser.items('ducks'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'ducks', str(datkey))
        continue
    cnfwrite('duckhunt.cnf', 'ducks', 'cache', '0')
    time.sleep(0.1)
    for name, value in parser.items('bedazzled'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'bedazzled', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('soggy'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'soggy', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('sabotage'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'sabotage', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('expl_ammo'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'expl_ammo', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('gun_grease'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'gun_grease', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('trigger_lock'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'trigger_lock', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('sunglasses'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'sunglasses', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('silencer'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'silencer', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('lucky_charm'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'lucky_charm', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('accident_insurance'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'accident_insurance', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('rain_coat'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'rain_coat', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('duck_bomb'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'duck_bomb', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('bread_lock'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'bread_lock', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('popcorn'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'popcorn', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('bombed'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'bombed', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('duck_jam'):
        datkey = '%s' % name
        cnfdelete('duckhunt.cnf', 'duck_jam', str(datkey))
        continue
    time.sleep(0.1)
    return
# ===> statreset

# FUNCTION #============================================================================================================
# Name...........: timeconvertmsg
# Description....: Converts a seconds value into X hours X minutes statement (needs work)
# Syntax.........: timeconvertmsg(tseconds)
# Parameters.....: tseconds = the time value in seconds
# Return values..: Returns 'X hours X minutes X seconds' as a string statement
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def timeconvertmsg(tseconds):
    ttime = round(tseconds)
    hours = 0
    if int(ttime) < 3600:
        hours = 0
    if int(ttime) >= 3600:
        hours = int(ttime) / 3600
    ttime = int(ttime) % int(3600)
    minutes = int(ttime) / 60
    seconds = int(ttime) % 60
    if numtok(str(hours), '.') > 1:
        hours = gettok(str(hours), 0, '.')
    if numtok(str(minutes), '.') > 1:
        minutes = gettok(str(minutes), 0, '.')
    if numtok(str(seconds), '.') > 1:
        seconds = gettok(str(seconds), 0, '.')
    return str(hours) + ' hours ' + str(minutes) + ' minutes ' + str(seconds) + ' seconds'
# ===> timeconvertmsg

# FUNCTION #============================================================================================================
# Name...........: tshotplus
# Description....: Increases the total shots data for 1 shot
# Syntax.........: tshotplus()
# Parameters.....: None
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def tshotplus():
    global daily
    daily = cnfread('duckhunt.cnf', 'top_shot', 'daily')
    global weekly
    weekly = cnfread('duckhunt.cnf', 'top_shot', 'weekly')
    global monthly
    monthly = cnfread('duckhunt.cnf', 'top_shot', 'monthly')
    global totalshot
    totalshot = cnfread('duckhunt.cnf', 'top_shot', 'totalshot')
    daily = int(daily) + 1
    cnfwrite('duckhunt.cnf', 'top_shot', 'daily', str(daily))
    weekly = int(weekly) + 1
    cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', str(weekly))
    monthly = int(monthly) + 1
    cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', str(monthly))
    totalshot = int(totalshot) + 1
    cnfwrite('duckhunt.cnf', 'top_shot', 'totalshot', str(totalshot))
    return
# ===> tshotplus

# FUNCTION #============================================================================================================
# Name...........: userdat
# Description....: used for defined maintenance /msg botname maint user <xp/level> <data>
#                  removes user entries based on xp or level.
# Syntax.........: userdat(idtype, data)
# Parameters.....: idtype = xp or level
#                  data = Number for xp or level (will delete entries less than or equal to data)
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def userdat(idtype, data):
    parser = RawConfigParser()
    parser.read('duckhunt.cnf')

    for name, value in parser.items('ducks'):
        datkey = '%s' % name
        # print('DATKEY: ' + str(datkey))
        if str(datkey) == 'cache':
            continue
        xp = duckinfo(datkey, b'xp')
        level = duckinfo(datkey, b'level')
        if idtype == 'xp':
            if int(xp) <= int(data):
                cnfdelete('duckhunt.cnf', 'ducks', datkey)
                continue
        if idtype == 'level':
            if int(level) <= int(data):
                cnfdelete('duckhunt.cnf', 'ducks', datkey)
                continue
        continue
    return
# ===> userdat

# FUNCTION #============================================================================================================
# Name...........: striptext
# Description....: remove IRC colors from text
# Syntax.........: striptext(text)
# Parameters.....: text = String to strip colors from
# Return values..: Returns = text string with color coding removed
# Author.........: ComputerTech
# Modified.......: Neo_Nemesis
# ======================================================================================================================
def striptext(txtdat):
    stripper = re.compile(r'\x03(?:\d{1,2}(?:,\d{1,2})?)?', re.UNICODE)
    return stripper.sub('', txtdat)
# ==> striptext

# CNF FILE FUNCTIONS
# FUNCTION #============================================================================================================
# Name...........: cnfdelete
# Description....: Deletes a key from the specified section
# Syntax.........: cnfdelete(file, section, key)
# Parameters.....: file = path and filename (only include path if file is not in script directory)
#                  section = section_name found in .cnf file
#                  key = key to be deleted
# Return values..: True - key deleted
#                  False - key not found/doesn't exist
# ======================================================================================================================
def cnfdelete(file, section, key):
    config = configparser.ConfigParser()
    config.read(file)
    if config.has_option(section, key):
        config.remove_option(section, key)
        with open(file, 'w') as conf:
            config.write(conf)
            return True
    return False
# ===> cnfdelete

# FUNCTION #============================================================================================================
# Name...........: cnfexists
# Description....: Determines if specified information exists in a .cnf file
# Syntax.........: cnfexists(file, section, key)
# Parameters.....: file = path and filename (only include path if file is not in script directory)
#                  section = section_name found in .cnf file
#                  key = key_name from specified section
# Return values..: True - value exists
#                  False - value does not exist
# ======================================================================================================================
def cnfexists(file, section, key):
    config = configparser.ConfigParser()
    config.read(file)
    if config.has_option(section, key):
        return True
    else:
        return False
# ===> cnfexists

# FUNCTION #============================================================================================================
# Name...........: cnfread
# Description....: Reads data from .cnf files. Section and key MUST exist in file, or will result in error.
# Syntax.........: cnfread(file, section, key)
# Parameters.....: file = path and filename (only include path if file is not in script directory)
#                  section = section_name found in .cnf file
#                  key = key_name from specified section
# Return values..: Returns the data from the specified section key
# ======================================================================================================================
def cnfread(file, section, key):
    config_object = ConfigParser()
    config_object.read(file)
    info = config_object[section]
    return format(info[key])
# ===> cnfread

# FUNCTION #============================================================================================================
# Name...........: cnfwrite
# Description....: Writes data to .cnf files
# Syntax.........: cnfwrite(file, section, key, data)
# Parameters.....: file = path and filename (only include path if file is not in script directory)
#                  section = section_name found in .cnf file
#                  key = key_name from specified section
#                  data = information to be written
# Return values..: None
# ======================================================================================================================
def cnfwrite(file, section, key, data):
    config_object = ConfigParser()
    config_object.read(file)
    info = config_object[section]
    info[key] = data
    with open(file, 'w') as conf:
        config_object.write(conf)
# ===> cnfwrite

# FUNCTION #============================================================================================================
# Name...........: addtok
# Description....: Adds a token to the end of a token string
# Syntax.........: addtok(string, token, char)
# Parameters.....: string = the token string
#                  token = token to be added
#                  char = seperator character
# Return values..: Returns the string with new token added
# Example........: addtok('A,B,C,D,E', 'F', ',') - Returns 'A,B,C,D,E,F'
# ======================================================================================================================
def addtok(string, token, char):
    atok = string + char + token
    return atok
# ===> addtok

# FUNCTION #============================================================================================================
# Name...........: deltok
# Description....: Deletes all occurences of a token from a token string
# Syntax.........: deltok(string, token, char)
# Parameters.....: string = token string to be analyzed
#                  token = token value to be removed
#                  char = seperator character
# Return values..: Returns the token string with specified token occurances removed
# Example........: deltok('Z,A,B,Z,C,D,E', 'Z', ',') - Returns 'A,B,C,D,E'
# ======================================================================================================================
def deltok(string, token, char):
    data = string.split(char)
    newstring = ''
    x = 0
    for x in range(len(data)):
        if data[x] == token:
            continue
        if data[x] != token:
            if newstring == '':
                newstring = data[x]
                continue
            if newstring != '':
                newstring = newstring + char + data[x]
                continue
    return newstring
# ===> deltok

# FUNCTION #============================================================================================================
# Name...........: gettok
# Description....: Retrieves a token from a token string
# Syntax.........: gettok(string, x, char)
# Parameters.....: string = the token string
#                  x = the token slot in the string
#                  char = seperator character
# Return values..: returns the specified token from the string
# Remarks........: PLEASE NOTE x: First token A is 0, second B is 1 etc.
#                  Tokens A-Z can be any value seperated by any seperator char
#                  Most common is char 44 = ','
# Example........: gettok('A,B,C,D', '2', ',') - Returns "C"
# ======================================================================================================================
def gettok(string, x, char):
    data = string.split(char)
    return data[x]
# ===> gettok

# FUNCTION #============================================================================================================
# Name...........: istok
# Description....: determines if a token exists in a token string
# Syntax.........: istok(string, token, char)
# Parameters.....: string = token string to be analyzed
#                  token = token to be matched
#                  char = seperator character
# Return values..: Token exists in string: True
#                  Token does not exist: False
# Example........: istok('A,B,C,D,E', 'D', ',') - Returns True
#                  istok('A,B,C,D,E', 'F', ',') - Returns False
# ======================================================================================================================
def istok(string, token, char):
    dat = string.split(char)
    x = 0
    for x in range(len(dat)):
        if dat[x] == token:
            return True
        else:
            x += 1
            continue
    return False
# ===> istok

# FUNCTION #============================================================================================================
# Name...........: numtok
# Description....: Determines the total number of tokens in a string
# Syntax.........: numtok(string, char)
# Parameters.....: string = the token string to be counted
#                  char = seperator character
# Return values..: Returns an intenger of tokens
# Example........: numtok('A,B,C,D,E', ',') - Returns 5
# ======================================================================================================================
def numtok(string, char):
    dat = string.split(char)
    return len(dat)
# ===> numtok

# FUNCTION #============================================================================================================
# Name...........: reptok
# Description....: Replaces a token in a token string
# Syntax.........: reptok(string, x, char, tok)
# Parameters.....: string = the token string
#                  x = the token slot in the string
#                  char = seperator character
#                  tok = new token data to insert
# Return values..: returns the string with new token
# Remarks........: PLEASE NOTE: First token is #0, second is #1 etc.
# Example........: reptok('A,B,C,D', '2', ',', 'X') - Returns "A,B,X,D"
# ======================================================================================================================
def reptok(string, x, char, tok):
    data = string.split(char)
    z = 0
    newstring = ''
    for z in range(len(data)):
        if z == x:
            if newstring == '':
                newstring = tok
                z += 1
                continue
            if newstring != '':
                newstring = newstring + char + tok
                z += 1
                continue
        if z != x:
            if newstring == '':
                newstring = data[z]
                z += 1
                continue
            if newstring != '':
                newstring = newstring + char + data[z]
                z += 1
                continue
        continue
    return newstring
# ===> reptok

# FUNCTION #============================================================================================================
# Name...........: hour1
# Description....: Returns 1 hour in seconds
# Syntax.........: hour1()
# Parameters.....: None
# Return values..: Returns 3600
# ======================================================================================================================
def hour1():
    return 3600
    # return 120
# ===> hour1

# FUNCTION #============================================================================================================
# Name...........: hour24
# Description....: Returns 24 hours in seconds
# Syntax.........: hour24()
# Parameters.....: None
# Return values..: Returns 86400
# ======================================================================================================================
def hour24():
    return 86400
    # return 120
# ===> hour24

# FUNCTION #============================================================================================================
# Name...........: hourtosec
# Description....: Convert hours to seconds
# Syntax.........: hourtosec(hours)
# Parameters.....: hours - number of hours to be converted
# Return values..: Returns the seconds value of input hours
# Example........: hourtosec(24) --> returns 86400
# ======================================================================================================================
def hourtosec(hours):
    timeval = int(hours) * 60
    seconds = int(timeval) * 60
    return str(seconds)
# ===> hourtosec
# Mode60 https://m0de-60.github.io/web - SDH1.1.4 Final