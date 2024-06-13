import csv
import re

import numpy
import requests
from bs4 import BeautifulSoup

'''爬取城市数据并写入city.txt文件'''
'''需要手动删除4个直辖市的重复数据'''
# 城市人口数量
num_list = []
# 城市名称
name_list = []
sheng_list = []
i = 0
r = requests.get('https://www.citypopulation.de/zh/china/admin/')
soup = BeautifulSoup(r.text, 'html.parser')
names = soup.find_all(class_='rname')
nums = soup.find_all(class_='rpop')
for num in nums:
    i += 1
    if i % 3 == 0:
        num_list.append(num.string)
# 人口数量
num_list = num_list[1:-6]

for name in names:
    if name.string is not None:
        content = name.string
        if content[-1] in ['省', '区', '市', '州', '盟', '划']:
            name_list.append(content)
        if content[-1] == '省' or content in ['上海市', '重庆市', '北京市', '天津市'] or content[:2] in ['新疆', '广西',
                                                                                                         '西藏', '宁夏',
                                                                                                         '内蒙']:
            sheng_list.append(content)
# with open('./city.txt', 'w', encoding='utf-8') as f:
#     for name, num in zip(name_list, num_list):
#         if name[-1] == '省' or name in ['上海市', '重庆市', '北京市', '天津市'] or name[:2] in ['新疆', '广西','西藏', '宁夏','内蒙']:
#             f.write('\n')
#         f.write(f'{name},{num},')

'''创建各省的txt文件'''
# for name in name_list:
#     if name[-1] == '省':
#         with open(f'./txt/{name}.txt', 'w') as f:
#             pass
#     elif name in ['上海市', '重庆市', '北京市', '天津市']:
#         with open(f'./txt/{name}.txt', 'w') as f:
#             pass
#     elif name[:2] in ['新疆', '广西', '西藏', '宁夏', '内蒙']:
#         with open(f'./txt/{name}.txt', 'w') as f:
#             pass


'''写入数据'''
with open(f'finally_chart/data/txt/city.txt', 'r', encoding='utf-8') as f:
    cities = []
    data = csv.reader(f)
    for row in data:
        cities.append(row[:-1])  # 总数据(row[:-1]去除空数据)
    for name in cities:
        for val in name:
            if val[-1] == '省' or val in ['上海市', '重庆市', '北京市', '天津市'] or val[:2] in ['新疆', '广西', '西藏',
                                                                                                 '宁夏', '内蒙']:
                with open(f'finally_chart/data/txt/{val}.txt', 'w', encoding='utf-8') as f:
                    str = ','.join(name)
                    f.write(str)
