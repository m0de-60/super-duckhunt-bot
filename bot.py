# ABOUT INFO# ==========================================================================================================
# Title..........: Super DuckHunt v1.0 Python IRC Bot (BETA)
# File...........: bot.py (bot script dependant functions)
# Python version.: v3.12.0 (does not work in older versions)
# Script version.: v1.0
# Language.......: English
# Description....: IRC Bot Script based off original DuckHunt bot by Menz Agitat
#                  Lots of changes and twists added to this, following suit as Menz Agitat bot was said to be a "port"
#                  of the NES game for IRC, This one would be equivelent to a SNES version, or a "sequel".
# Imports........: func.py, time
# Author(s)......: Neo_Nemesis (aka coderusa, Neo`Nemesis)
# Modified.......:
# Contributors...: bildramer, Friithian, ComputerTech, esjay, TheFatherMind, [Neo from Freenode], End3r
# ======================================================================================================================
import func
import time
# CURRENT FUNCTIONS LIST - SEE FUNCTION SECTION FOR DESCRIPTIONS =======================================================
# data_check
# duckinfo
# iecheck
# inveffect
# isaccess
# isbotmaster
# shopprice
# timeconvertmsg
# ======================================================================================================================
# noinspection PySimplifyBooleanCheck

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
        timem = time.time() - float(timem)
        if type == 'gun_grease':
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'gun_grease', user)
                return
        if type == 'trigger_lock':
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'trigger_lock', user)
                return
        if type == 'silencer':
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'silencer', user)
                return
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
        if type == 'duck_bomb':
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'duck_bomb', user)
                return
        if type == 'bedazzled':
            if timem >= float(func.hour1()):
                func.cnfdelete('duckhunt.cnf', 'bedazzled', user)
                return
        if type == 'soggy':
            if timem >= float(func.hour1()):
                func.cnfdelete('duckhunt.cnf', 'soggy', user)
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
    if func.cnfexists('duckhunt.cnf', 'trigger_lock', user) == True:
        timem = func.cnfread('duckhunt.cnf', 'trigger_lock', user)
        timem = time.time() - float(timem)
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'trigger_lock', user)
# silencer check =======================================================================================================
    if func.cnfexists('duckhunt.cnf', 'silencer', user) == True:
        timem = func.cnfread('duckhunt.cnf', 'silencer', user)
        timem = time.time() - float(timem)
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'silencer', user)
# lucky charm check ====================================================================================================
    if func.cnfexists('duckhunt.cnf', 'lucky_charm', user) == True:
        timem = func.cnfread('duckhunt.cnf', 'lucky_charm', user)
        timem = time.time() - float(timem)
        if timem >= float(func.hour24()):
            func.cnfdelete('duckhunt.cnf', 'lucky_charm', user)
# gun grease check =====================================================================================================
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
        if func.cnfexists('duckhunt.cnf', 'duck_bomb', user) == True:
            timem = func.cnfread('duckhunt.cnf', 'duck_bomb', user)
            timem = time.time() - float(timem)
            if timem >= float(func.hour24()):
                func.cnfdelete('duckhunt.cnf', 'duck_bomb', user)
# soggy check =====================================================================================================
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
    if func.cnfexists('duckhunt.cnf', 'gun_grease', str(user)) == True:
        huntingbag = 'Gun Grease'
    if func.cnfexists('duckhunt.cnf', 'trigger_lock', str(user)) == True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' | ' + 'Gun Lock'
        if huntingbag == '0':
            huntingbag = 'Gun Lock'
    if func.cnfexists('duckhunt.cnf', 'silencer', str(user)) == True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' | ' + 'Silencer'
        if huntingbag == '0':
            huntingbag = 'Silencer'
    if func.cnfexists('duckhunt.cnf', 'lucky_charm', str(user)) == True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' | ' + 'Lucky Charm'
        if huntingbag == '0':
            huntingbag = 'Lucky Charm'
    if func.cnfexists('duckhunt.cnf', 'sunglasses', str(user)) == True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' | ' + 'Sunglasses'
        if huntingbag == '0':
            huntingbag = 'Sunglasses'
    if func.cnfexists('duckhunt.cnf', 'accident_insurance', str(user)) == True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' | ' + 'Accident Insurance'
        if huntingbag == '0':
            huntingbag = 'Accident Insurance'
    if func.cnfexists('duckhunt.cnf', 'rain_coat', str(user)) == True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' | ' + 'Rain Coat'
        if huntingbag == '0':
            huntingbag = 'Rain Coat'
    if huntingbag != '0':
        huntingbag = '[HUNTING BAG] ' + huntingbag
    if huntingbag == '0':
        huntingbag = '[HUNTING BAG] None'
    if func.cnfexists('duckhunt.cnf', 'bedazzled', str(user)) == True:
        if effects != '0':
            effects = effects + ' | ' + 'Bedazzled'
        if effects == '0':
            effects = 'Bedazzled'
    if func.cnfexists('duckhunt.cnf', 'soggy', str(user)) == True:
        if effects != '0':
            effects = effects + ' | ' + 'Soggy'
        if effects == '0':
            effects = 'Soggy'
    if effects != '0':
        effects = '[EFFECTS] ' + effects
    if effects == '0':
        effects = '[EFFECTS] None'
    return huntingbag + ' ' + effects
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
# Name...........: shopprice
# Description....: Determines price of specified item. Change price values here
#                  Item prices vary based on user stats, for !shop
# Syntax.........: shopprice(user, itemid)
# Parameters.....: user - name of user who is using !shop
#                  itemid - !shop ID of the item.
# Return values..: Returns the specified price of the item
#                  Returns 0 if unknown/invalid itemid specified
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def shopprice(user, itemid):
    # data prep
    ammo = duckinfo(user, b'ammo')
    mrounds = func.gettok(ammo, 2, '?')
    mmags = func.gettok(ammo, 3, '?')

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
    # gun grease
    if int(itemid) == 3:
        return 15
    # magazine upgrade
    if int(itemid) == 4:
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
    # return confiscated gun
    if int(itemid) == 5:
        return 30
    # gun cleaning
    if int(itemid) == 6:
        return 30
    # gun uprade
    if int(itemid) == 7:
        return 200
    # Gun Lock
    if int(itemid) == 8:
        return 15
    # silencer
    if int(itemid) == 9:
        return 15
    # lucky charm
    if int(itemid) == 10:
        return 30
    # sunglasses
    if int(itemid) == 11:
        return 20
    # dry clothes
    if int(itemid) == 12:
        return 15
    # additional magazine
    if int(itemid) == 13:
        if int(mmags) == 3:
            return 50
        if int(mmags) >= 4:
            return 70
    # mirror
    if int(itemid) == 14:
        return 20
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
        return 15
    if int(itemid) == 20:
        return 20
    # unkown item/ID
    return 0
# ===> shopprice

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
    print(str(tseconds))
    time = round(tseconds)
    if int(time) < 3600:
        hours = 0
    if int(time) >= 3600:
        hours = int(time) / 3600
    time = int(time) % int(3600)
    minutes = int(time) / 60
    seconds = int(time) % 60
    if func.numtok(str(hours), '.') > 1:
        hours = func.gettok(str(hours), 0, '.')
    if func.numtok(str(minutes), '.') > 1:
        minutes = func.gettok(str(minutes), 0, '.')
    if func.numtok(str(seconds), '.') > 1:
        seconds = func.gettok(str(seconds), 0, '.')
    return str(hours) + ' hours ' + str(minutes) + ' minutes ' + str(seconds) + ' seconds'
# ===> timeconvertmsg
