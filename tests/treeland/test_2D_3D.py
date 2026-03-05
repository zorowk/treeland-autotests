# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
特效切换
"""
import pyautogui
from time import sleep


def test_tab_action():
    # while True:
    # pyautogui.hotkey('alt', 'tab')
    pyautogui.keyDown('winleft')
    pyautogui.keyDown('shift')
    pyautogui.press('tab', presses=4, interval=2)
    pyautogui.keyUp('winleft')
    pyautogui.keyUp('shift')
    sleep(1)

    # screenshot
    # pyautogui.hotkey('ctrl', 'alt', 'a')
    # sleep(2)
    # pyautogui.hotkey('enter')
