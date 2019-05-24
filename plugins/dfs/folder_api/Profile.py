import configparser
import os

from DFS_folder.settings import inifilepath


def readprofile(title,key):
    try:
        conf = configparser.ConfigParser()
        conf.read(os.path.join(inifilepath,"config.ini"))
        returnvalue = conf.get(title, key)
        return returnvalue
    except Exception as e:
        return False

def writeprofile(title,key,value):
    try:
        conf = configparser.ConfigParser()
        conf.read(os.path.join(inifilepath,"config.ini"))
        conf.set(title, key,value)
        conf.write(open(os.path.join(inifilepath,"config.ini"), "w"))
        return True
    except Exception as e:
        return False

