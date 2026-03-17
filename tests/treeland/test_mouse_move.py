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
    result = subprocess.run(['wlr-randr'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Unable to run wlr-randr: {result.stderr}")
        return

    output = result.stdout
    current_scale = 1.0
    current_resolution = None

    for line in output.splitlines():
        line = line.strip()

        if line.startswith("Scale:"):
            try:
                current_scale = float(line.split(":", 1)[1].strip())
            except:
                current_scale = 1.0
            continue

        if "current" in line and re.match(r'^\s*\d+x\d+', line):
            res_match = re.match(r'^\s*(\d+)x(\d+)', line)
            if res_match:
                width = int(res_match.group(1))
                height = int(res_match.group(2))
                current_resolution = (width, height)
                break

    if current_resolution:
        x = int(current_resolution[0] * current_scale)
        y = int(current_resolution[1] * current_scale)
    else:
        print("Unable to find current resolution from wlr-randr.")
        return

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
