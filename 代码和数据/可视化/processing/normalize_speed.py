import csv
import os
import numpy as np 


data_path = os.path.abspath(r'E:\_Code\Html\map\static\data\东湖绿道\data.csv')

data = []
with open(data_path, encoding='utf-8') as f:
    csv_reader_lines = csv.reader(f)
    for one_line in csv_reader_lines:
        data.append(one_line)

name = data[0]
data = data[1:]

mmax = np.max([float(data[i][4]) for i in range(len(data))])

for line in data:
    line.append(round(float(line[4]) / mmax * 255))

name.append('normalized_speed')
out_data = [name] + data

# 输出成csv文件
with open(data_path, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(out_data)