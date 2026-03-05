# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
mouse move
"""
import os
import random
import pyautogui
import datetime,time
import re


def test_mouse_move():
    hd = os.popen('xrandr | grep connected').read().split(' ')
    screen = []
    try:
        i = hd.index('connected')
    except ValueError:
        i = -1
    while i != -1 and i + 1 < len(hd):
        info = re.split('[x]|[+]', hd[i + 1])
        if len(info) == 4:
            screen.append([int(info[0]), int(info[1]), int(info[2]), int(info[3])])
        try:
            i = hd.index('connected', i + 1) #从 i+1 位置开始向后查收connected字符串的位置下标，没找到则返回-1
        except ValueError:
            i = -1
    if len(screen) == 0:
        return
    starttime = datetime.datetime.now()
    endtime = datetime.datetime.now()
    while (endtime - starttime).seconds <= 1:
        n = random.randint(0, len(screen) - 1)
        w, h, x, y = screen[n]
        x1 = random.randint(x, x + w)
        y1 = random.randint(y, y + h - 80)
        pyautogui.moveTo(x1, y1, duration=0.1)
        pyautogui.click()
        endtime = datetime.datetime.now()





