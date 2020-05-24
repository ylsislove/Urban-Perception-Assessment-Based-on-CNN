import WebCoordSystemTransform
import csv
import os

matedata_path = os.path.abspath(r'E:\_SpatialData\GIS-Q4\Q4-未来屯-20200101_200125\VID_20200101_200125.csv')
output_data = os.path.abspath(r'E:\_SpatialData\GIS-Q4\Q4-未来屯-20200101_200125\data.csv')

wt = WebCoordSystemTransform.WebCoordSystemTransform()

data = []
with open(matedata_path, encoding='utf-8') as f:
    csv_reader_lines = csv.reader(f)
    for one_line in csv_reader_lines:
        # 获取到纬度和经度
        # print(one_line[2], one_line[3])
        # 进行转换
        if not data:
            # data.append([one_line[0], one_line[2], one_line[3]])
            data.append(one_line)
        else:
            mgLat, mgLon = wt.wgs2gcj(float(one_line[1]), float(one_line[2]))
            one_line[1], one_line[2] = mgLat, mgLon
            # data.append([one_line[0], mgLat, mgLon])
            data.append(one_line)

# 输出成csv文件
with open(output_data, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
