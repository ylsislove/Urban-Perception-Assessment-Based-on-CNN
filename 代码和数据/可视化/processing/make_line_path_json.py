import csv
import json
import os

csv_path = os.path.abspath(r'E:\_Code\Html\map\static\data\scores.csv')
json_path = os.path.abspath(r'E:\_Code\Html\map\static\data\line.json')

data_list = []
with open(csv_path, mode='r', encoding='utf-8') as f:
    csv_lines = csv.reader(f)
    for line in csv_lines:
        data_list.append(line)

data_list = data_list[1:]

data_dict = {}
data_dict['data'] = dict()
data_dict['data']['name'] = 'path1'
data_dict['data']['path'] = []

for line in data_list:
    data_dict['data']['path'].append([line[2], line[1]])

# 先将字典对象转化为可写入文本的字符串
json_str = json.dumps(data_dict, indent=4)

# 写入文件
with open(json_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_str)
