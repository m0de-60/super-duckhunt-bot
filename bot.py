#! /usr/bin/python3
# ABOUT INFO# ==========================================================================================================
# Title..........: Super DuckHunt v1.1 Python IRC Bot (BETA)
# File...........: bot.py (bot script dependant functions)
# Python version.: v3.12.0 (does not work in older versions)
# Script version.: v1.1.0
# Language.......: English
# Description....: IRC Bot Script based off original DuckHunt bot by Menz Agitat
#                  Lots of changes and twists added to this, following suit as Menz Agitat bot was said to be a "port"
#                  of the NES game for IRC, This one would be equivelent to a SNES version, or a "sequel".
# Imports........: func.py, time
# Author(s)......: Neo_Nemesis (aka coderusa, Neo`Nemesis)
# Modified.......:
# Contributors...: bildramer, Friithian, ComputerTech, esjay, TheFatherMind, [Neo from Freenode], End3r
# ======================================================================================================================
from configparser import RawConfigParser
import func
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
def debug(mode, data, ext=''):
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
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'expl_ammo', str(datkey))
            continue
    time.sleep(0.1)
    for name, value in parser.items('sabotage'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'sabotage', str(datkey))
            continue
    time.sleep(0.1)
    for name, value in parser.items('trigger_lock'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'trigger_lock', str(datkey))
            continue
    time.sleep(0.1)
    for name, value in parser.items('bread_lock'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'bread_lock', str(datkey))
            continue
    time.sleep(0.1)
    for name, value in parser.items('duck_jam'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'duck_jam', str(datkey))
            continue
    time.sleep(0.1)
    for name, value in parser.items('gun_grease'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'gun_grease', str(datkey))
            continue
        dat = func.cnfread('duckhunt.cnf', 'gun_grease', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if float(timem) >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'gun_grease', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('silencer'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'silencer', str(datkey))
            continue
        dat = func.cnfread('duckhunt.cnf', 'silencer', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'silencer', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('lucky_charm'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'lucky_charm', str(datkey))
            continue
        dat = func.gettok(func.cnfread('duckhunt.cnf', 'lucky_charm', str(datkey)), 0, ',')
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'lucky_charm', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('sunglasses'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'sunglasses', str(datkey))
            continue
        dat = func.cnfread('duckhunt.cnf', 'sunglasses', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'sunglasses', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('accident_insurance'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'accident_insurance', str(datkey))
            continue
        dat = func.cnfread('duckhunt.cnf', 'accident_insurance', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'accident_insurance', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('rain_coat'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'rain_coat', str(datkey))
            continue
        dat = func.cnfread('duckhunt.cnf', 'rain_coat', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'rain_coat', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('duck_bomb'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'duck_bomb', str(datkey))
            continue
        dat = func.gettok(func.cnfread('duckhunt.cnf', 'duck_bomb', str(datkey)), 0, ',')
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'duck_bomb', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('bedazzled'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'bedazzled', str(datkey))
            continue
        dat = func.cnfread('duckhunt.cnf', 'bedazzled', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(func.hour1()):
            func.cnfdelete('duckhunt.cnf', 'bedazzled', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('soggy'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'soggy', str(datkey))
            continue
        dat = func.cnfread('duckhunt.cnf', 'soggy', str(datkey))
        timem = time.time() - float(dat)
        # print(str(datkey) + ' TIME: ' + str(timem))
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'soggy', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('bombed'):
        datkey = '%s' % name
        if not func.cnfexists('duckhunt.cnf', 'ducks', str(datkey)):
            func.cnfdelete('duckhunt.cnf', 'bombed', str(datkey))
            continue
    time.sleep(0.1)
    return
# ===> cnfcleanup

# FUNCTION #============================================================================================================
# Name...........: data_check
# Description....: checks and handles items/effects time entries. This function also doubles as invetory/effects
#                  retreival for !duckstats, and used to determine if user has certain item in their inventory,
#                  replacing the use of b'inv' and b'effects' in duckinfo().
# Syntax.........: data_check(user, type, ext)
# Parameters.....: user - username to be checked
#                  type - Time entry type (see remarks)
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
def data_check(user, type, ext=''):
    if ext == 'add':
        func.cnfwrite('duckhunt.cnf', type, user, str(time.time()))
        return True
    elif ext == 'del':
        if func.cnfexists('duckhunt.cnf', type, user) == False:
            return False
        func.cnfdelete('duckhunt.cnf', type, user)
        return True
    elif ext == 'get':
        if func.cnfexists('duckhunt.cnf', type, user) == False:
            return False
        if func.cnfexists('duckhunt.cnf', type, user) == True:
            return func.cnfread('duckhunt.cnf', type, user)
        return False
    elif ext == '' and func.cnfexists('duckhunt.cnf', type, user):
        timem = func.cnfread('duckhunt.cnf', type, user)
        # update 1.1.0 - for lucky charm and expansion and duck bomb recode
        if func.numtok(str(timem), ',') > 1:
            timem = func.gettok(str(timem), 0, ',')
        # # # ===
        timem = time.time() - float(timem)
        if type == 'gun_grease':
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'gun_grease', user)
                return
        # update 1.1.0 - removed 24 hour parameter for Gun Lock
        # if type == 'trigger_lock':
        #     if timem >= float(func.hour24()):
        #         func.cnfdelete('duckhunt.cnf', 'trigger_lock', user)
        #         return
        if type == 'silencer':
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'silencer', user)
                return
        # update 1.1.0 - lucky charm change, now stored in token string " time,lcxp "
        if type == 'lucky_charm':
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'lucky_charm', user)
                return
        if type == 'sunglasses':
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'sunglasses', user)
                return
        if type == 'accident_insurance':
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'accident_insurance', user)
                return
        if type == 'rain_coat':
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'rain_coat', user)
                return
        # update v1.1.0 - restructured duck bomb code for !bomb recode
        if type == 'duck_bomb':
            bombent = func.gettok(func.cnfread('duckhunt.cnf', 'duck_bomb', user), 1, ',')
            if int(bombent) == 0 and timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'duck_bomb', user)
                return
            if int(bombent) > 0 and timem >= float(func.hour24()):
                func.cnfwrite('duckhunt.cnf', 'duck_bomb', user, str(time.time()) + ',0')
                return
        if type == 'bedazzled':
            if timem >= float(func.hour1()):
                func.cnfdelete('duckhunt.cnf', 'bedazzled', user)
                return
        if type == 'soggy':
            if timem >= float(func.hour1()):
                func.cnfdelete('duckhunt.cnf', 'soggy', user)
                return
        # explosive ammo, update 1.1.0
        if type == 'expl_ammo':
            if func.cnfexists('duckhunt.cnf', 'expl_ammo', str(user)):
                uself = func.cnfread('duckhunt.cnf', 'expl_ammo', str(user))
                if int(uself) == 0:
                    func.cnfdelete('duckhunt.cnf', 'expl_ammo', str(user))
                    return
        # popcorn ammo, update 1.1.0
        if type == 'popcorn':
            if func.cnfexists('duckhunt.cnf', 'popcorn', str(user)):
                popl = func.cnfread('duckhunt.cnf', 'popcorn', str(user))
                if int(popl) == 0:
                    func.cnfdelete('duckhunt.cnf', 'popcorn', str(user))
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
    cnfdat = func.cnfread('duckhunt.cnf', 'ducks', str(user))
    if req == b'ammo':
        if data == '':
            return func.gettok(cnfdat, 0, ',')
        else:
            duck_info = func.reptok(cnfdat, 0, ',', data)
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'ducks':
        if data == '':
            return func.gettok(cnfdat, 1, ',')
        else:
            duck_info = func.reptok(cnfdat, 1, ',', str(data))
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'gducks':
        if data == '':
            return func.gettok(cnfdat, 2, ',')
        else:
            duck_info = func.reptok(cnfdat, 2, ',', data)
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'xp':
        if data == '':
            return func.gettok(cnfdat, 3, ',')
        else:
            duck_info = func.reptok(cnfdat, 3, ',', str(data))
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'level':
        if data == '':
            return func.gettok(cnfdat, 4, ',')
        else:
            duck_info = func.reptok(cnfdat, 4, ',', data)
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'levelup':
        if data == '':
            return func.gettok(cnfdat, 5, ',')
        else:
            duck_info = func.reptok(cnfdat, 5, ',', data)
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'effects':
        if data == '':
            return func.gettok(cnfdat, 6, ',')
        else:
            duck_info = func.reptok(cnfdat, 6, ',', data)
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'inv':
        if data == '':
            return func.gettok(cnfdat, 7, ',')
        else:
            duck_info = func.reptok(cnfdat, 7, ',', data)
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'guninfo':
        if data == '':
            return func.gettok(cnfdat, 8, ',')
        else:
            duck_info = func.reptok(cnfdat, 8, ',', data)
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'best':
        if data == '':
            return func.gettok(cnfdat, 9, ',')
        else:
            duck_info = func.reptok(cnfdat, 9, ',', data)
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'accidents':
        if data == '':
            return func.gettok(cnfdat, 10, ',')
        else:
            duck_info = func.reptok(cnfdat, 10, ',', data)
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'bread':
        if data == '':
            return func.gettok(cnfdat, 11, ',')
        else:
            duck_info = func.reptok(cnfdat, 11, ',', data)
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
            return 1
    if req == b'friend':
        if data == '':
            return func.gettok(cnfdat, 12, ',')
        else:
            duck_info = func.reptok(cnfdat, 12, ',', data)
            func.cnfwrite('duckhunt.cnf', 'ducks', str(user), duck_info)
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
    if func.cnfexists('duckhunt.cnf', 'ducks', str(user)) == False:
        return
# gun grease check =====================================================================================================
    if func.cnfexists('duckhunt.cnf', 'gun_grease', user) == True:
        timem = func.cnfread('duckhunt.cnf', 'gun_grease', user)
        timem = time.time() - float(timem)
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'gun_grease', user)
# Gun Lock check ===================================================================================================
# update 1.1.0 - removed 24 hour parameter and replaced with different parameters
#    if func.cnfexists('duckhunt.cnf', 'trigger_lock', user) == True:
#        timem = func.cnfread('duckhunt.cnf', 'trigger_lock', user)
#        timem = time.time() - float(timem)
#        if timem >= float(func.hour24()):
#            func.cnfdelete('duckhunt.cnf', 'trigger_lock', user)
# silencer check =======================================================================================================
    if func.cnfexists('duckhunt.cnf', 'silencer', user) == True:
        timem = func.cnfread('duckhunt.cnf', 'silencer', user)
        timem = time.time() - float(timem)
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'silencer', user)
# lucky charm check ====================================================================================================
    # update 1.1.0 - lucky charm now stored as token string " time,lcxp "
    if func.cnfexists('duckhunt.cnf', 'lucky_charm', user) == True:
        timem = func.gettok(func.cnfread('duckhunt.cnf', 'lucky_charm', user), 0, ',')
        timem = time.time() - float(timem)
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'lucky_charm', user)
# sunglasses check =====================================================================================================
    if func.cnfexists('duckhunt.cnf', 'sunglasses', user) == True:
        timem = func.cnfread('duckhunt.cnf', 'sunglasses', user)
        timem = time.time() - float(timem)
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'sunglasses', user)
# accident insurance check =============================================================================================
    if func.cnfexists('duckhunt.cnf', 'accident_insurance', user) == True:
        timem = func.cnfread('duckhunt.cnf', 'accident_insurance', user)
        timem = time.time() - float(timem)
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'accident_insurance', user)
# rain coat check ======================================================================================================
    if func.cnfexists('duckhunt.cnf', 'rain_coat', user) == True:
        timem = func.cnfread('duckhunt.cnf', 'rain_coat', user)
        timem = time.time() - float(timem)
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'rain_coat', user)
# duck bomb check ======================================================================================================
    # update 1.1.0 restructured duck bomb for !bomb recode ENTRY: b'username' = time,X
    #                                                             X = bomb uses, if X = 0 then no bombs for 24 hrs
    if func.cnfexists('duckhunt.cnf', 'duck_bomb', user) == True:
        bombent = func.gettok(func.cnfread('duckhunt.cnf', 'duck_bomb', user), 1, ',')
        if int(bombent) == 0:
            timem = func.gettok(func.cnfread('duckhunt.cnf', 'duck_bomb', user), 0, ',')
            timem = time.time() - float(timem)
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'duck_bomb', user)
        if int(bombent) > 0:
            timem = func.gettok(func.cnfread('duckhunt.cnf', 'duck_bomb', user), 0, ',')
            timem = time.time() - float(timem)
            if timem >= float(func.hour24()):
                func.cnfwrite('duckhunt.cnf', 'duck_bomb', user, str(time.time()) + ',0')
# soggy check ==========================================================================================================
    if func.cnfexists('duckhunt.cnf', 'soggy', user) == True:
        timem = func.cnfread('duckhunt.cnf', 'soggy', user)
        timem = time.time() - float(timem)
        if timem >= float(func.hour1()):
            func.cnfdelete('duckhunt.cnf', 'soggy', user)
# bedazzled check ======================================================================================================
    if func.cnfexists('duckhunt.cnf', 'bedazzled', user) == True:
        timem = func.cnfread('duckhunt.cnf', 'bedazzled', user)
        timem = time.time() - float(timem)
        if timem >= float(func.hour1()):
            func.cnfdelete('duckhunt.cnf', 'bedazzled', user)
# expl ammo check ======================================================================================================
    # update 1.1.0
    if func.cnfexists('duckhunt.cnf', 'expl_ammo', user) == True:
        expl = func.cnfread('duckhunt.cnf', 'expl_ammo', user)
        if int(expl) == 0:
            func.cnfdelete('duckhunt.cnf', 'expl_ammo', user)
# popcorn check ========================================================================================================
    # update 1.1.0
    if func.cnfexists('duckhunt.cnf', 'popcorn', user) == True:
        pop = func.cnfread('duckhunt.cnf', 'popcorn', user)
        if int(pop) == 0:
            func.cnfdelete('duckhunt.cnf', 'popcorn', user)
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
    if func.cnfexists('duckhunt.cnf', 'gun_grease', str(user)) == True:
        huntingbag = '\x037,1Gun Grease'
    # gun lock
    if func.cnfexists('duckhunt.cnf', 'trigger_lock', str(user)) == True:
        invuse = func.cnfread('duckhunt.cnf', 'trigger_lock', str(user))
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Gun Lock \x034,1[' + str(invuse) + ']'
        if huntingbag == '0':
            huntingbag = '\x037,1Gun Lock\x034,1 [' + str(invuse) + ']'
    # silencer
    data_check(str(user), 'silencer')
    if func.cnfexists('duckhunt.cnf', 'silencer', str(user)) == True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Silencer'
        if huntingbag == '0':
            huntingbag = '\x037,1Silencer'
    # lucky charm
    data_check(str(user), 'lucky_charm')
    if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(user)) == True:
        invuse = func.gettok(func.cnfread('duckhunt.cnf', 'lucky_charm', str(user)), 1, ',')
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 Lucky Charm \x034,1[+' + str(invuse) + 'xp]'
        if huntingbag == '0':
            huntingbag = '\x037,1Lucky Charm \x034,1[+' + str(invuse) + 'xp]'
    # sunglasses
    data_check(str(user), 'sunglasses')
    if func.cnfexists('duckhunt.cnf', 'sunglasses', str(user)) == True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Sunglasses'
        if huntingbag == '0':
            huntingbag = '\x037,1Sunglasses'
    # accident insurance
    data_check(str(user), 'accident_insurance')
    if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(user)) == True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Accident Insurance'
        if huntingbag == '0':
            huntingbag = '\x037,1Accident Insurance'
    # rain coat
    data_check(str(user), 'rain_coat')
    if func.cnfexists('duckhunt.cnf', 'rain_coat', str(user)) == True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Rain Coat'
        if huntingbag == '0':
            huntingbag = '\x037,1Rain Coat'
    # v.1.1.0 for bread expansion
    if func.cnfexists('duckhunt.cnf', 'bread_lock', str(user)) == True:
        invuse = func.cnfread('duckhunt.cnf', 'bread_lock', str(user))
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 Bread Box Lock \x034,1[' + str(invuse) + ']'
        if huntingbag == '0':
            huntingbag = '\x037,1Bread Box Lock \x034,1[' + str(invuse) + ']'
    # v.1.1.0 expl ammo
    data_check(str(user), 'expl_ammo')
    if func.cnfexists('duckhunt.cnf', 'expl_ammo', str(user)) == True:
        expl = func.cnfread('duckhunt.cnf', 'expl_ammo', str(user))
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 Explosive Ammo \x034,1[' + str(expl) + ']'
        if huntingbag == '0':
            huntingbag = '\x037,1Explosive Ammo \x034,1[' + str(expl) + ']'
    # v.1.1.0 bag of popcorn
    data_check(str(user), 'popcorn')
    if func.cnfexists('duckhunt.cnf', 'popcorn', str(user)) == True:
        pop = func.cnfread('duckhunt.cnf', 'popcorn', str(user))
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
    if func.cnfexists('duckhunt.cnf', 'bedazzled', str(user)) == True:
        if effects != '0':
            effects = effects + ' \x030,1|\x037,1 ' + 'Bedazzled'
        if effects == '0':
            effects = '\x037,1Bedazzled'
    # soggy
    data_check(str(user), 'soggy')
    if func.cnfexists('duckhunt.cnf', 'soggy', str(user)) == True:
        if effects != '0':
            effects = effects + ' \x030,1|\x037,1 ' + 'Soggy'
        if effects == '0':
            effects = '\x037,1Soggy'
    # sabotaged
    if func.cnfexists('duckhunt.cnf', 'sabotage', str(user)) == True:
        if effects != '0':
            effects = effects + ' \x030,1|\x037,1 ' + 'Sabotage'
        if effects == '0':
            effects = '\x037,1Sabotage'
    # bombed
    if func.cnfexists('duckhunt.cnf', 'bombed', str(user)) == True:
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
    admin = func.cnfread('duckhunt.cnf', 'duckhunt', 'admin')
    # print(admin)
    botmaster = func.cnfread('duckhunt.cnf', 'duckhunt', 'botmaster')
    # print(botmaster)
    if func.istok(str(admin), str(user), ',') == True:
        return True
    if func.istok(str(botmaster), str(user), ',') == True:
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
    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'maxducks', '6')
    global maxducks
    maxducks = 6

    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'spawntime', '1800')
    global spawntime
    spawntime = 1800

    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'flytime', '1500')
    global flytime
    flytime = 1500

    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'duckexp', '15')
    global duckexp
    duckexp = 15

    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'duckfear', '45')
    global duckfear
    duckfear = 45

    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'duckgold', '40')
    global duckgold
    duckgold = 40

    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'friendrate', '70')
    global friendrate
    friendrate = 71

    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'floodcheck', '24,25')
    global flood_check
    flood_check = True

    func.cnfwrite('duckhunt.cnf', 'rules', 'gunricochet', '5')
    global gunricochet
    gunricochet = 5

    func.cnfwrite('duckhunt.cnf', 'rules', 'thebushes', '15')
    global thebushes
    thebushes = 15

    func.cnfwrite('duckhunt.cnf', 'rules', 'gunconf', 'on')
    global gunconf
    gunconf = 'on'

    func.cnfwrite('duckhunt.cnf', 'rules', 'infammo', 'off')
    global infammo
    infammo = 'off'

    func.cnfwrite('duckhunt.cnf', 'rules', 'bang', 'on')
    global bang
    bang = 'on'

    func.cnfwrite('duckhunt.cnf', 'rules', 'bef', 'on')
    global bef
    bef = 'on'

    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'maint', '24')
    global maint
    maint = '24'

    func.cnfwrite('duckhunt.cnf', 'duckhunt', 'maint_time', str(time.time()))
    global maint_time
    maint_time = str(time.time())

    time.sleep(0.10)

    parser = RawConfigParser()
    parser.read('duckhunt.cnf')

    for name, value in parser.items('flood_protection'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'flood_protection', str(datkey))
        continue

    time.sleep(0.10)

    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!bang', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!duckstats', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!shop', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!bef', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!reload', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!bomb', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!tshot', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!mshot', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!help', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!swim', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!wshot', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!dshot', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!about', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!topduck', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!reloaf', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '!bread', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '\x01version\x01', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '\x01finger\x01', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', '\x01ping', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', 'version', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', 'finger', 'True')
    func.cnfwrite('duckhunt.cnf', 'flood_protection', 'ping', 'True')

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
    func.cnfwrite('duckhunt.cnf', 'top_shot', 'daily', '0')
    global daily
    daily = '0'

    func.cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', '0')
    global weekly
    weekly = '0'

    func.cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', '0')
    global monthly
    monthly = '0'

    func.cnfwrite('duckhunt.cnf', 'top_shot', 'totalshot', '0')
    global totalshot
    totalshot = '0'

    func.cnfwrite('duckhunt.cnf', 'top_shot', 't_day', '1')
    func.cnfwrite('duckhunt.cnf', 'top_shot', 't_week', '1')
    func.cnfwrite('duckhunt.cnf', 'top_shot', 't_month', '1')
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
    bang = func.cnfread('duckhunt.cnf', 'rules', 'bang')
    global bef
    bef = func.cnfread('duckhunt.cnf', 'rules', 'bef')

    rounds = func.gettok(ammo, 0, '?')
    mrounds = func.gettok(ammo, 2, '?')
    mags = func.gettok(ammo, 1, '?')
    mmags = func.gettok(ammo, 3, '?')

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
            return str(srchtxt) + ' a fishing weight. \x033Better luck next time.\x03'

        if int(rounds) < int(mrounds):
            rounds = int(rounds) + 1
            ammo = str(rounds) + '?' + str(mags) + '?' + str(mrounds) + '?' + str(mmags)
            duckinfo(user, b'ammo', ammo)
            return str(srchtxt) + ' an extra bullet. \x033[Rounds: ' + str(rounds) + '/' + str(mrounds) + ' | Magazines: ' + str(mags) + '/' + str(mmags) + '\x03'

    if int(srch) == 6:
        data_check(str(user), 'lucky_charm')
        if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(user)):
            xp = int(xp) + 5
            duckinfo(str(user), b'xp', str(xp))
            return str(srchtxt) + ' a duck feather. \x033[+5 xp]\x03'

        if not func.cnfexists('duckhunt.cnf', 'lucky_charm', str(user)):
            found = 'Lucky Charm'
            lcxp = random.randint(3, 8)
            func.cnfwrite('duckhunt.cnf', 'lucky_charm', str(user), str(time.time()) + ',' + str(lcxp))
            return str(srchtxt) + ' a Lucky Charm. \x033You will earn an extra ' + str(lcxp) + ' xp for every duck for 24 hrs.\x03'

    if int(srch) == 7:
        found = 'Golden Duck Feather'
        xp = int(xp) + 150
        duckinfo(str(user), b'xp', str(xp))
        return str(srchtxt) + ' a golden duck feather. \x033[+150 xp]\x03'

    if int(srch) == 8:
        found = 'Frog'
        xp = int(xp) + 25
        duckinfo(str(user), b'xp', str(xp))
        return str(srchtxt) + ' a frog. * RIBBIT * \x033[+25 xp]\x03'

    if int(srch) == 9:
        found = 'Sunglasses'
        func.cnfwrite('duckhunt.cnf', 'sunglasses', str(user), str(time.time()))
        return str(srchtxt) + ' a pair of Sunglasses. \x033You are now protected from bedazzlement for 24 hours.\x03'

    if int(srch) == 10:
        xp = int(xp) + 25
        duckinfo(str(user), b'xp', str(xp))
        return str(srchtxt) + ' a frog. * RIBBIT * \x033[+25 xp]\x03'

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
    mrounds = func.gettok(ammo, 2, '?')
    mmags = func.gettok(ammo, 3, '?')
    guninfo = duckinfo(user, b'guninfo')
    accuracy = func.gettok(guninfo, 0, '?')
    mreliability = func.gettok(guninfo, 2, '?')
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
        if int(mreliability) > 80 and int(mreliability) < 85:
            return 35
        if int(mreliability) >= 85 and int(mreliability) < 90:
            return 40
        if int(mreliability) >= 90 and int(mreliability) < 95:
            return 45
        if int(mreliability) >= 95 and int(mreliability) <= 100:
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
        if int(accuracy) > 90 and int(accuracy) < 100 and int(mreliability) >= 100:
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
        if func.cnfexists('duckhunt.cnf', 'soggy', str(user.lower())) is False and func.cnfexists('duckhunt.cnf', 'bombed', str(user.lower())) is False:
            return 25
        if func.cnfexists('duckhunt.cnf', 'soggy', str(user.lower())) is True and func.cnfexists('duckhunt.cnf', 'bombed', str(user.lower())) is False:
            return 25
        if func.cnfexists('duckhunt.cnf', 'soggy', str(user.lower())) is False and func.cnfexists('duckhunt.cnf', 'bombed', str(user.lower())) is True:
            return 50
        if func.cnfexists('duckhunt.cnf', 'soggy', str(user.lower())) is True and func.cnfexists('duckhunt.cnf', 'bombed', str(user.lower())) is True:
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
        func.cnfdelete('duckhunt.cnf', 'ducks', str(datkey))
        continue
    func.cnfwrite('duckhunt.cnf', 'ducks', 'cache', '0')
    time.sleep(0.1)
    for name, value in parser.items('bedazzled'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'bedazzled', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('soggy'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'soggy', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('sabotage'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'sabotage', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('expl_ammo'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'expl_ammo', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('gun_grease'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'gun_grease', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('trigger_lock'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'trigger_lock', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('sunglasses'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'sunglasses', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('silencer'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'silencer', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('lucky_charm'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'lucky_charm', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('accident_insurance'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'accident_insurance', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('rain_coat'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'rain_coat', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('duck_bomb'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'duck_bomb', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('bread_lock'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'bread_lock', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('popcorn'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'popcorn', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('bombed'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'bombed', str(datkey))
        continue
    time.sleep(0.1)
    for name, value in parser.items('duck_jam'):
        datkey = '%s' % name
        func.cnfdelete('duckhunt.cnf', 'duck_jam', str(datkey))
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
    # if func.numtok(str(time), '.') == 1:
    #     hour = math.ceil(time)
    #     min = 0
    # if func.numtok(str(time), '.') > 1:
    #    hour = func.gettok(str(time), 0, '.')
    #    min = '.' + func.gettok(str(time), 1, '.')
    #    min = func.hourtomin(float(min))
    # return str(hour) + ' hours ' + str(min) + ' minutes'
    # print(str(tseconds))
    ttime = round(tseconds)
    hours = 0
    if int(ttime) < 3600:
        hours = 0
    if int(ttime) >= 3600:
        hours = int(ttime) / 3600
    ttime = int(ttime) % int(3600)
    minutes = int(ttime) / 60
    seconds = int(ttime) % 60
    if func.numtok(str(hours), '.') > 1:
        hours = func.gettok(str(hours), 0, '.')
    if func.numtok(str(minutes), '.') > 1:
        minutes = func.gettok(str(minutes), 0, '.')
    if func.numtok(str(seconds), '.') > 1:
        seconds = func.gettok(str(seconds), 0, '.')
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
    daily = func.cnfread('duckhunt.cnf', 'top_shot', 'daily')
    global weekly
    weekly = func.cnfread('duckhunt.cnf', 'top_shot', 'weekly')
    global monthly
    monthly = func.cnfread('duckhunt.cnf', 'top_shot', 'monthly')
    global totalshot
    totalshot = func.cnfread('duckhunt.cnf', 'top_shot', 'totalshot')
    daily = int(daily) + 1
    func.cnfwrite('duckhunt.cnf', 'top_shot', 'daily', str(daily))
    weekly = int(weekly) + 1
    func.cnfwrite('duckhunt.cnf', 'top_shot', 'weekly', str(weekly))
    monthly = int(monthly) + 1
    func.cnfwrite('duckhunt.cnf', 'top_shot', 'monthly', str(monthly))
    totalshot = int(totalshot) + 1
    func.cnfwrite('duckhunt.cnf', 'top_shot', 'totalshot', str(totalshot))
    return
# ===> tshotplus

# FUNCTION #============================================================================================================
# Name...........: userdat
# Description....: used for defined maintenance /msg botname maint user <xp/level> <data>
#                  removes user entries based on xp or level.
# Syntax.........: userdat(type, data)
# Parameters.....: type = xp or level
#                  data = Number for xp or level (will delete entries less than or equal to data)
# Return values..: None
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def userdat(type, data):
    parser = RawConfigParser()
    parser.read('duckhunt.cnf')

    for name, value in parser.items('ducks'):
        datkey = '%s' % name
        # print('DATKEY: ' + str(datkey))
        if str(datkey) == 'cache':
            continue
        xp = duckinfo(datkey, b'xp')
        level = duckinfo(datkey, b'level')
        if type == 'xp':
            if int(xp) <= int(data):
                func.cnfdelete('duckhunt.cnf', 'ducks', datkey)
                continue
        if type == 'level':
            if int(level) <= int(data):
                func.cnfdelete('duckhunt.cnf', 'ducks', datkey)
                continue
        continue
    return
# ===> userdat
