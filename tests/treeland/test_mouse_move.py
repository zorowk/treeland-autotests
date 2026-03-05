# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
mouse move
"""
import random
import re
import subprocess
import datetime
import pyautogui

def test_mouse_move():
    # 运行命令并获取输出
    result = subprocess.run(['xrandr'], capture_output=True, text=True)
    output = result.stdout
    # 使用正则表达式查找当前模式的分辨率
    matchs = re.findall(r'(\d+) x (\d+)', output)
    if matchs:
        x = matchs[1][0]
        y = matchs[1][1]
    else:
        print("Unable to find current resolution.")

    starttime = datetime.datetime.now()
    while(True):
        endtime = datetime.datetime.now()
        if((endtime - starttime).seconds > 1):
            break
        else:
            x1 = random.randint(0, int(x))
            y1 = random.randint(0, int(y)-80)
            pyautogui.moveTo(x1, y1, duration=0.1)
            pyautogui.click()


    # starttime = datetime.datetime.now()
    # endtime = datetime.datetime.now()
    # while (endtime - starttime).seconds <= 1:
    #     x1 = random.randint(0, int(x))
    #     y1 = random.randint(0, int(y)-80)
    #     pyautogui.moveTo(x1, y1, duration=0.1)
    #     pyautogui.click()
    #     endtime = datetime.datetime.now()