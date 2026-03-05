# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
tab action
"""
import pyautogui
from time import sleep

def test_tab_action():
    # while True:
    # pyautogui.hotkey('alt', 'tab')

    pyautogui.keyDown('alt')
    pyautogui.press('tab', presses=6, interval=0.2)
    pyautogui.keyUp('alt')
    sleep(1)

# screenshot
# pyautogui.hotkey('ctrl', 'alt', 'a')
# sleep(2)
# pyautogui.hotkey('enter')
test_tab_action()