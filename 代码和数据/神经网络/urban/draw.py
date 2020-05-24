import matplotlib.pyplot as plt
import numpy as np
import os
import csv

mode = 'wealthy'
input_path = os.path.abspath(r'E:\_Code\Tensorflow\urban-emotion-recognition\urber\model_dir\{}\{}_out.csv'.format(mode, mode))

data = []
if os.path.exists(input_path):
    with open(input_path, mode='r', encoding='utf-8') as f:
        csv_lines = csv.reader(f)
        for line in csv_lines:
            data.append(line)
else:
    print('path is wrong')

epoch = [i[0] for i in data]
epoch = np.asarray(epoch[1:], dtype='uint16')
loss = [i[1] for i in data]
loss = np.asarray(loss[1:], dtype='float64')
mae = [i[2] for i in data]
mae = np.asarray(mae[1:], dtype='float64')
val_loss = [i[3] for i in data]
val_loss = np.asarray(val_loss[1:], dtype='float64')
val_mae = [i[4] for i in data]
val_mae = np.asarray(val_mae[1:], dtype='float64')


plt.figure(num=1, figsize=(8, 6))

ax1 = plt.subplot(211)
l1, = plt.plot(epoch, loss, color='red', label='loss')
l2, = plt.plot(epoch, val_loss, color='blue', label='val_loss')
plt.legend(handles=[l1, l2], loc='best')
plt.xlabel('epoch')
plt.ylabel('loss')

ax2 = plt.subplot(212)
l3, = plt.plot(epoch, mae, color='red', label='mae')
l4, = plt.plot(epoch, val_mae, color='blue', label='val_mae')
plt.legend(handles=[l3, l4], loc='best')
plt.xlabel('epoch')
plt.ylabel('mae')

ax1.set_title("{}".format(mode))

plt.tight_layout()
plt.show()