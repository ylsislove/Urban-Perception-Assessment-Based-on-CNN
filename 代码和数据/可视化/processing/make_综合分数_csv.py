import csv
import os
import numpy as np 


data_path = os.path.abspath(r'E:\_Code\Html\map\static\data\光谷老校区\data.csv')

data = []
with open(data_path, encoding='utf-8') as f:
    csv_reader_lines = csv.reader(f)
    for one_line in csv_reader_lines:
        data.append(one_line)

name = data[0]
data = data[1:]

mmax = np.max([float(data[i][4]) for i in range(len(data))])

for line in data:
    score = float(line[11]) + (100 - float(line[12])) + (100 - float(line[13])) + float(line[14]) + float(line[15]) + float(line[16])
    line.append(round(score / 6))

name.append('Combined_Score1')
out_data = [name] + data

# 输出成csv文件
with open(data_path, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(out_data)