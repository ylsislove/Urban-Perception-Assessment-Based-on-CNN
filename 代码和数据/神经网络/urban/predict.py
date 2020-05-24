#导入所有的依赖包
import  tensorflow as tf
import numpy as np
import os
from PIL import Image
import csv

def read_csv(file_path):
    data = []
    with open(file_path, encoding='utf-8') as f:
        csv_reader_lines = csv.reader(f)
        for one_line in csv_reader_lines:
            data.append(one_line)
    return data

def create_model(model_name):
    model_name = r'E:\_Code\Tensorflow\urban-emotion-recognition\urber\model_dir\{}\cnn_model.h5'.format(model_name)
    # 判断是否已经有model文件存在，如果model文件存在则加载原来的model并在原来的moldel继续训练，如果不存在则新建model相关文件
    if os.path.exists(model_name):
        # 如果存在模型文件，则加载存放model文件夹中最新的文件
        print("Reading model parameters from %s" % model_name)
        # 使用tf.keras.models.load_model来加载模型
        model = tf.keras.models.load_model(model_name)
        return model
    else:
        print("There is no model")
        exit(0)

# 定义预测函数
def predict(model, data):
    # 使用predict方法对输入数据进行预测
    prediction = model.predict(data)
    # 返回预测结果
    return prediction[0][0]

def run(model, image_path):
    dirs = os.listdir(image_path)
    data = []
    iii = 1
    for f in dirs:
        filename = os.path.join(image_path, f)
        # 使用PIL中的Image打开文件并获取图像文件中的信息
        img = Image.open(filename)
        # 缩放图片的尺寸
        img = img.resize((480, 300))
        # 将图像文件的格式转换为RGB
        img = img.convert("RGB")
        # 分别获取r,g,b三元组的像素数据并进行拼接
        r, g, b = img.split()
        r_arr = np.array(r)
        g_arr = np.array(g)
        b_arr = np.array(b)
        img = np.concatenate((r_arr, g_arr, b_arr))
        # 将拼接得到的数据按照模型输入维度需要转换为（300, 480, 3)，并对数据进行归一化
        image = img.reshape([1, 300, 480, 3])/255
        # 调用predict方法进行预测
        result = predict(model, image)
        print(iii, result)
        data.append([f, result])
        iii += 1
    return data

if __name__ == "__main__":

    # 'beautiful', 'boring', 'depressing', 'lively', 'safety', 'wealthy'
    image_types = ['wealthy']
    image_path = os.path.abspath(r'E:\_SpatialData\GIS-Q4\Q4-东湖绿道-20200102_150503\images')
    file_path = os.path.abspath(r'E:\_SpatialData\GIS-Q4\Q4-东湖绿道-20200102_150503\VID_20200102_150503.csv')
    outfile_path = os.path.abspath(r'E:\_SpatialData\GIS-Q4\Q4-东湖绿道-20200102_150503\VID_20200102_150503.csv')

    src_data = read_csv(file_path)
    src_name = src_data[0]
    src_data = src_data[1:]

    for image_type in image_types:
        # 初始化model
        model = create_model(image_type)
        predict_data = run(model, image_path)
        print('{}模型预测完毕'.format(image_type))

        src_name.append(image_type)
        for line in predict_data:
            filename = line[0].replace('_', ':')[:-8]
            # print(filename)
            for d in src_data:
                if d[0][11:19] == filename:
                    d.append(line[1])

    out_data = [src_name] + src_data
    # 输出成csv文件
    with open(outfile_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(out_data)
