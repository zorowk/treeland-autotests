# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
聚合了一些日常操作场景

"""
import os
import random
import subprocess

import pyautogui
import datetime
import time


def test_move_window():
    """移动窗口"""
    # 打开窗口选择移动
    pyautogui.hotkey('ctrl', 'alt', 't')
    time.sleep(1)
    pyautogui.hotkey('alt', 'space')
    time.sleep(0.5)
    for i in range(3):
        pyautogui.hotkey('down')
    pyautogui.press('enter')
    # 移动窗口
    hd = os.popen('xrandr | grep current').read().split(',')[1]
    x = hd.split(' ')[2]
    y = hd.split(' ')[4]
    star_t = datetime.datetime.now()
    end_t = datetime.datetime.now()
    while (end_t - star_t).seconds <= 5:
        x1 = random.randint(0, int(x))
        y1 = random.randint(0, int(y)-40)
        pyautogui.moveTo(x1, y1, duration=0.1)
        end_t = datetime.datetime.now()
    pyautogui.hotkey('esc')
    time.sleep(1)
    pyautogui.hotkey('alt', 'f4')


def test_mouse_move():
    # 随机移动鼠标
    hd = os.popen('xrandr | grep current').read().split(',')[1]
    x = hd.split(' ')[2]
    y = hd.split(' ')[4]
    starttime = datetime.datetime.now()
    endtime = datetime.datetime.now()
    while (endtime - starttime).seconds <= 5:
        x1 = random.randint(0, int(x))
        y1 = random.randint(0, int(y)-40)
        pyautogui.moveTo(x1, y1, duration=0.1)
        pyautogui.click()
        endtime = datetime.datetime.now()


def test_tab_action():
    # 切换Alt+tab
    for i in range(3):
        pyautogui.keyDown('alt')
        pyautogui.press('tab', presses=8, interval=0.2)
        pyautogui.keyUp('alt')
        time.sleep(1)


def test_openbrowser():
    """打开浏览器输入内容"""
    subprocess.Popen('bash -c browser', shell=True)
    time.sleep(2)
    pyautogui.typewrite("https://pms.uniontech.com/bug-browse-111.html")
    time.sleep(2)
    pyautogui.hotkey("enter")
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
#
#
# def test_ScreenResolution_switch():
#     """切换屏幕分辨率"""
#     # 暂时写死的方式
#     subprocess.Popen("xrandr --output Virtual-1 --mode 1024x768", shell=True)
#     time.sleep(5)
#     subprocess.Popen("xrandr --output Virtual-1 --mode 1920x1080", shell=True)
#     time.sleep(5)
#     subprocess.Popen("xrandr --output Virtual-1 --mode 1920x1040", shell=True)
#     time.sleep(5)
    # 本地调试数据
    # subprocess.Popen("xrandr --output HDMI-A-0 --mode 1440x900", shell=True)
    # time.sleep(5)
    # subprocess.Popen("xrandr --output HDMI-A-0 --mode 1024x768", shell=True)
    # time.sleep(5)
    # subprocess.Popen("xrandr --output HDMI-A-0 --mode 1920x1080", shell=True)
    # time.sleep(5)