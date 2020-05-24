import os
import json
import csv

data_path = os.path.abspath(r'E:\_Code\Html\map\static\data\光谷老校区\data.csv')
output_path = os.path.abspath(r'E:\_Code\Html\map\static\data\光谷老校区\heatMap.json')

src_data = []
out_data = []
with open(data_path, mode='r', encoding='utf-8') as f:
    csv_lines = csv.reader(f)
    for line in csv_lines:
        src_data.append(line)

data_name = src_data[0]
src_data = src_data[1:]

for line in src_data:
    a = dict()
    for i in range(len(data_name)):
        if i == 2 or i == 3 or i == 24:
            a[data_name[i]] = line[i]
    out_data.append(a)
    # out_data.append({data_name[-1]:line[-1]})

print(len(out_data))

# 先将字典对象转化为可写入文本的字符串
json_str = json.dumps(out_data, ensure_ascii=False, indent=4)

# 写入文件
with open(output_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_str)
