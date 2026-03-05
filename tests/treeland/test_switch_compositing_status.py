#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
:Author:yuanrui@uniontech.com
:Date  :2024/7/15 上午10:12
"""

import pyautogui
import time
import logging

'切换窗口特效及alt+tab切换'

def test_switch_compositing_status():
    # while True:
    # pyautogui.hotkey('alt', 'tab')
    pyautogui.keyDown('winleft')
    pyautogui.keyDown('shift')
    pyautogui.press('tab', presses=2, interval=2)
    pyautogui.keyUp('winleft')
    pyautogui.keyUp('shift')

    LOOP_TIMES = 3  #循环次数
    for i in range(LOOP_TIMES):
        retry_count = 3  # 设置重试次数
        try:
            pyautogui.keyDown('alt')
            for _ in range(retry_count):
                try:
                    pyautogui.press('tab', presses=3, interval=0.2)
                    break  # 如果成功则跳出重试循环
                except Exception as e:
                    logging.error(f"Error during tab press in retry {_ + 1}: {e}")
                    time.sleep(0.5)  # 等待一小段时间再重试
            pyautogui.keyUp('alt')
        except Exception as e:
            logging.error(f"Error in key operations: {e}")
    time.sleep(1)
    pyautogui.keyDown('winleft')
    pyautogui.keyDown('shift')
    pyautogui.press('tab', presses=3, interval=2)
    pyautogui.keyUp('winleft')
    pyautogui.keyUp('shift')
    time.sleep(1)
    for i in range(LOOP_TIMES):
        retry_count = 3  # 设置重试次数
        try:
            pyautogui.keyDown('alt')
            for _ in range(retry_count):
                try:
                    pyautogui.press('tab', presses=3, interval=0.2)
                    break  # 如果成功则跳出重试循环
                except Exception as e:
                    logging.error(f"Error during tab press in retry {_ + 1}: {e}")
                    time.sleep(0.5)  # 等待一小段时间再重试
            pyautogui.keyUp('alt')
        except Exception as e:
            logging.error(f"Error in key operations: {e}")