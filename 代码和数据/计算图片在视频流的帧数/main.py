import os
import csv
import datetime
import json

matedata_path = os.path.abspath(r'E:\_SpatialData\GIS-Q4\Q4-东湖绿道-20200102_150503\VID_20200102_150503.csv')
out_path = os.path.abspath(r'E:\_SpatialData\GIS-Q4\Q4-东湖绿道-20200102_150503\data2frame.txt')
start_date = '2020-01-02 15:05:03:450'
d0 = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S:%f')

data_str = ''
if os.path.exists(matedata_path):
    with open(matedata_path, encoding='utf-8') as f:
        csv_reader_lines = csv.reader(f)
        i = 0
        for one_line in csv_reader_lines:
            i += 1
            if i == 1: continue
            # if i == 10: break
            # 获取到字符串时间
            date = one_line[0]
            # 格式化
            d1 = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S:%f')
            # 和开始时间计算出差值
            seconds = (d1 - d0).seconds + (d1 - d0).microseconds / 1000000
            # print(seconds)
            # 计算出帧数，原视频是1秒29.9729帧
            frame_num = round(seconds * 29.9996)
            # 保存成字符串
            data_str = data_str + date + ' ' + str(frame_num) + '\n'
        print('{} total lines : {:d}'.format(str(matedata_path), i))

else:
    print('matedata_path is wrong...' + matedata_path)
    exit(1)

# 写入文件
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(data_str)

