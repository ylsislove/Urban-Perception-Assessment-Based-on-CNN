import os
import json
import csv

data_path = os.path.abspath(r'E:\_Code\Html\map\static\data\光谷老校区\data.csv')
output_path = os.path.abspath(r'E:\_Code\Html\map\static\data\光谷老校区\scores.json')

src_data = []
out_data = []
with open(data_path, mode='r', encoding='utf-8') as f:
    csv_lines = csv.reader(f)
    for line in csv_lines:
        src_data.append(line)

src_data = src_data[1:]
print(len(src_data))

for line in src_data:
    item = []
    # item.append({"item":"beautiful", "阿宇":line[11], "尧大":line[18]})
    # item.append({"item":"boring", "阿宇":line[12], "尧大":line[19]})
    # item.append({"item":"depressing", "阿宇":line[13], "尧大":line[20]})
    # item.append({"item":"lively", "阿宇":line[14], "尧大":line[21]})
    # item.append({"item":"safety", "阿宇":line[15], "尧大":line[22]})
    # item.append({"item":"wealthy", "阿宇":line[16], "尧大":line[23]})
    # item.append({"item":"beautiful", "阿宇":round(float(line[11])), "尧大":round(float(line[18]))})
    # item.append({"item":"boring", "阿宇":round(float(line[12])), "尧大":round(float(line[19]))})
    # item.append({"item":"depressing", "阿宇":round(float(line[13])), "尧大":round(float(line[20]))})
    # item.append({"item":"lively", "阿宇":round(float(line[14])), "尧大":round(float(line[21]))})
    # item.append({"item":"safety", "阿宇":round(float(line[15])), "尧大":round(float(line[22]))})
    # item.append({"item":"wealthy", "阿宇":round(float(line[16])), "尧大":round(float(line[23]))})
    item.append({"item":"beautiful", "阿宇":round(float(line[11]))})
    item.append({"item":"boring", "阿宇":round(float(line[12]))})
    item.append({"item":"depressing", "阿宇":round(float(line[13]))})
    item.append({"item":"lively", "阿宇":round(float(line[14]))})
    item.append({"item":"safety", "阿宇":round(float(line[15]))})
    item.append({"item":"wealthy", "阿宇":round(float(line[16]))})
    out_data.append(item)

print(len(out_data))

# 先将字典对象转化为可写入文本的字符串
json_str = json.dumps(out_data, ensure_ascii=False, indent=4)

# 写入文件
with open(output_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_str)