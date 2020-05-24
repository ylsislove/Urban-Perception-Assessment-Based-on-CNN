#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, cv2
from pickled import *
from load import *
from image_resize import image_resize
from make_list import make_list

def make_data(image_type, mode, size):
  data_path = os.path.abspath(r'G:\scores\{}\src\{}\{}'.format(image_type, mode, size))
  file_list = os.path.abspath(r'G:\scores\{}\{}.lst'.format(image_type, mode))
  save_path = os.path.abspath(r'G:\scores\{}\bin\{}'.format(image_type, mode))
  data, label, lst = read_data(file_list, data_path)
  pickled(save_path, data, label, lst, bin_num = 1, mode=mode, size=('_'+size))


if __name__ == '__main__':
  image_types = ['safety', 'wealthy']
  modes = ['train', 'test']
  sizes = ['480_300', '480_320', '480_440', '480_640']
  for image_type in image_types:
    for mode in modes:
      image_resize(image_type, mode, 320)
      image_resize(image_type, mode, 440)
      image_resize(image_type, mode, 640)
      make_list(image_type, mode)
      for size in sizes:
        make_data(image_type, mode, size)


