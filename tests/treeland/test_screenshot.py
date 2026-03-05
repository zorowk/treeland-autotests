# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
1. 系统截图
"""
import time
import pyautogui
import os

def test_screenshot_wechat():
    # 1. 操作系统截图(设置截图路径默认为剪切板)
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'alt', 'a')
    time.sleep(1)
    # 鼠标移动
    pyautogui.moveTo(300, 300)
    time.sleep(1)
    pyautogui.dragTo(1200, 900)
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(2)
    cmd = 'rm -r ~/Desktop/*.jpg'
    os.system(cmd)
    time.sleep(0.5)

