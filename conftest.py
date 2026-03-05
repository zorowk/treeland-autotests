#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
'''
conftest.py 中定义的 fixture 可以被同一目录及其子目录下的所有测试文件使用，
可以在 conftest.py 中进行测试环境的配置，例如设置数据库连接、初始化测试数据等。
可以根据实际需求在 conftest.py 中编写自定义的 fixture 函数，以满足特定的测试场景。
pytest 会自动查找并加载项目中所有的 conftest.py 文件，无需在测试文件中显式导入。
'''
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import sys
# sys.path.append('/path/to/opencv-python')
