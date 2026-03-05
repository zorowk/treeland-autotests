#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
:Author:suncui@uniontech.com
:Date  :2023/9/1 下午1:52
"""
import pandas as pd

# 先执行test_cpu.sh脚本，生成~/top-cpu.txt文件
# 创建一个空的 DataFrame
df = pd.DataFrame(columns=['treeland_cpu:%'])

# 读取文本文件
# 将~/top-cpu.txt文件拿过来放到当前目录下
with open('~/top-cpu.txt', 'r') as file:
    lines = file.readlines()

# 解析每一行并提取第9个字段的值
for line in lines:
    fields = line.split()
    if len(fields) >= 9:
        field9 = fields[8]
        df.loc[len(df)] = [field9]

# 保存为 Excel 文件
df.to_excel('~/top-cpu-treeland.xlsx', index=False)
