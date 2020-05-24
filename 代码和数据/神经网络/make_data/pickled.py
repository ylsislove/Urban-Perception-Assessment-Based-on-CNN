#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import pickle

BIN_COUNTS = 5

def pickled(savepath, data, label, fnames, bin_num=BIN_COUNTS, mode="train", size=""):
  '''
    savepath (str): save path
    data (array): image data, a nx3072 array
    label (list): image label, a list with length n
    fnames (str list): image names, a list with length n
    bin_num (int): save data in several files
    mode (str): {'train', 'test'}
  '''
  assert os.path.isdir(savepath)
  total_num = len(fnames)
  samples_per_bin = total_num / bin_num
  assert samples_per_bin > 0
  idx = 0
  for i in range(bin_num): 
    start = int(i*samples_per_bin)
    end = int((i+1)*samples_per_bin)
    print(len(data[0]), start, end)
    if end <= total_num:
      dict = {'data': data[start:end, :],
              'labels': label[start:end],
              'filenames': fnames[start:end]}
    else:
      dict = {'data': data[start:, :],
              'labels': label[start:],
              'filenames': fnames[start:]}
    if mode == "train":
      dict['batch_label'] = "training batch {} of {}".format(idx, bin_num)
    else:
      dict['batch_label'] = "testing batch {} of {}".format(idx, bin_num)
      
    with open(os.path.join(savepath, 'data_batch_'+str(idx))+size, 'wb') as fi:
      pickle.dump(dict, fi)
    idx = idx + 1

