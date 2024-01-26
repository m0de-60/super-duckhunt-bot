#! /usr/bin/python3
# ABOUT INFO# ==========================================================================================================
# Title..........: Super DuckHunt v1.1.0 Python IRC Bot (BETA)
# File...........: func.py (random non-script dependant functions)
# File version...: v0.2
# Python version.: v3.12.0
# Script version.: v1.1.0+
# Remarks........: This is a multi-use UDF script. Can be used with any python script.
# Language.......: English
# Description....: A UDF of my own design based on what I needed to build Super-DuckHunt 1.0+ Has multiple functions
#                  using configparser, token strings, and time/time conversion. (See function list below)
# Imports........: configparser
# Author(s)......: Neo_Nemesis (aka coderusa, Neo`Nemesis)
# Modified.......:
# Contributors...: bildramer, Friithian, ComputerTech, esjay, TheFatherMind, [Neo from Freenode], End3r
# ======================================================================================================================
from configparser import ConfigParser
import configparser
# CURRENT FUNCTIONS LIST - SEE FUNCTION SECTION FOR DESCRIPTIONS =======================================================
# CNF FILE FUNCTIONS LIST #=============================================================================================
# cnfdelete
# cnfexists
# cnfread
# cnfwrite
# ======================================================================================================================
# TOKEN STRING FUNCTIONS LIST # ========================================================================================
# addtok
# deltok
# gettok
# istok
# numtok
# reptok
# ======================================================================================================================
# TIME & TIME CONVERSION FUNCTIONS LIST # ==============================================================================
# hour1
# hour24
# hourtomin
# hourtosec
# sectohour
# sectomin
# ======================================================================================================================

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
# Author.........: Neo_Nemesis
# Modified.......:
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
# Author.........: Neo_Nemesis
# Modified.......:
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
# Author.........: Neo_Nemesis
# Modified.......:
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
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def cnfwrite(file, section, key, data):
    config_object = ConfigParser()
    config_object.read(file)
    info = config_object[section]
    info[key] = data
    with open(file, 'w') as conf:
        config_object.write(conf)
# ===> cnfwrite

# TOKEN STRING FUNCTIONS
# FUNCTION #============================================================================================================
# Name...........: addtok
# Description....: Adds a token to the end of a token string
# Syntax.........: addtok(string, token, char)
# Parameters.....: string = the token string
#                  token = token to be added
#                  char = seperator character
# Return values..: Returns the string with new token added
# Author.........: Neo_Nemesis
# Modified.......:
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
# Author.........: Neo_Nemesis
# Modified.......:
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
# Author.........: Neo_Nemesis
# Remarks........: PLEASE NOTE x: First token A is 0, second B is 1 etc.
#                  Tokens A-Z can be any value seperated by any seperator char
#                  Most common is char 44 = ','
# Modified.......:
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
# Author.........: Neo_Nemesis
# Modified.......:
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
# Author.........: Neo_Nemesis
# Modified.......:
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
# Author.........: Neo_Nemesis
# Remarks........: PLEASE NOTE: First token is #0, second is #1 etc.
# Modified.......:
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

# TIME CONVERSION FUNCTIONS
# FUNCTION #============================================================================================================
# Name...........: hour1
# Description....: Returns 1 hour in seconds
# Syntax.........: hour1()
# Parameters.....: None
# Return values..: Returns 3600
# Author.........: Neo_Nemesis
# Modified.......:
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
# Author.........: Neo_Nemesis
# Modified.......:
# ======================================================================================================================
def hour24():
    return 86400
    # return 120
# ===> hour24

# FUNCTION #============================================================================================================
# Name...........: hourtomin
# Description....: Converts hours to minutes
# Syntax.........: hourtomin(hours)
# Parameters.....: hours - number of hours to convert to seconds
# Return values..: Returns the minutes value of input hour(s)
# Author.........: Neo_Nemesis
# Modified.......:
# Example........: hourtomin(2) - returns 120
# ======================================================================================================================
def hourtomin(hours):
    timeval = round(hours * 60)
    return timeval
# ===> hourtomin

# FUNCTION #============================================================================================================
# Name...........: hourtosec
# Description....: Convert hours to seconds
# Syntax.........: hourtosec(hours)
# Parameters.....: hours - number of hours to be converted
# Return values..: Returns the seconds value of input hours
# Author.........: Neo_Nemesis
# Modified.......:
# Example........: hourtosec(24) --> returns 86400
# ======================================================================================================================
def hourtosec(hours):
    timeval = int(hours) * 60
    seconds = int(timeval) * 60
    return str(seconds)
# ===> hourtosec
# FUNCTION #============================================================================================================
# Name...........: sectohour
# Description....: Converts seconds to hours
# Syntax.........: sectohour(seconds)
# Parameters.....: seconds - number of seconds to be converted
# Return values..: returns seconds converted to hours
# Author.........: Neo_Nemesis
# Modified.......:
# Example........: sectohour(60) - returns 1
# ======================================================================================================================
def sectohour(seconds):
    timeval = round(seconds / 3600, 2)
    return timeval
# ===> sectohour

# FUNCTION #============================================================================================================
# Name...........: sectomin
# Description....: Converts seconds to minutes
# Syntax.........: sectomin(seconds)
# Parameters.....: seconds - number of seconds to be converted
# Return values..: Returns the minutes value of input seconds
# Author.........: Neo_Nemesis
# Modified.......:
# Example........: sectomin(120) - returns 2
# ======================================================================================================================
def sectomin(seconds):
    timeval = round(seconds / 60, 2)
    return timeval
# ===> sectomin