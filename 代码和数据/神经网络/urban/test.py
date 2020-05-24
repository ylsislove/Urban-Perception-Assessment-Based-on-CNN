import tensorflow as tf
from cnnModel import cnnModel

import os
os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'  #注意修改你的路径

model=cnnModel(0.5)
model=model.createModel()
tf.keras.utils.plot_model(model, 'model.png')

