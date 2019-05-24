# @Time    : 2018/2/7 11:47
# @Author  :
import hashlib
from random import choice as randomChoice

from dfs.dbinfo import get_management_configuration
global password

passData = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
passData1=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

passData2 =['!', '@', '#', '$', '%', '&', '*']
passData3=['2', '3', '4', '5', '6', '7', '8', '9']


seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&*"

def genpwd():
    if get_management_configuration():
        pwdlengt=get_management_configuration()['lengthpwd']
    else:
        pwdlengt=4
    password = []
    password.append(randomChoice(passData))
    password.append(randomChoice(passData1))
    password.append(randomChoice(passData2))
    password.append(randomChoice(passData3))
    for i in range(int(pwdlengt)-4):
        password.append(randomChoice(seed))
    salt = ''.join(password)
    # x = 0
    # p = ''
    # while x != len(password):
    #     p = p + str(password[x])
    #     x += 1
    return salt



