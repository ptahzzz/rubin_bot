import datetime as dt
from lists import *


def converted_date(data, flag):
    data = dt.datetime.strptime(data, '%m-%d')
    data = f"{data:%j}"
    if flag:
        return int(data)
    else:
        return zodiac_sign(data)


def zodiac_sign(date):
    if date[0] == '0':
        date = date[1::]
    date = int(date)
    flag = True
    if flag:
        for znak in list_zod:
            if znak != 'козерог':
                if (date >= list_zod[znak][0]) and (date <= list_zod[znak][1]):
                    return znak
            else:
                return znak

def minimal_razn(a):
    key_znach_list = []
    minimal = 10 ** 4
    for key in list_zod_com:
        for znach in list_zod_com[key]:
            rasn = abs(a - znach[1])
            if rasn < minimal:
                minimal = rasn
                key_znach_list = [key, znach[0]]
    return key_znach_list[1]


def music_text(name):
    file = open(f' songs/{name}', encoding="utf8").read()
    return file
