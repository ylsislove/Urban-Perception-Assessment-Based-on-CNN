#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import pickle

mode = 'test'


def unpickled(filename):
    assert os.path.isfile(filename)
    with open(filename, 'rb') as fo:
        dict = pickle.load(fo)
    return dict


def compare(dict1, dict2):
    for i in range(len(dict1)):
        if dict1[i] != dict2[i]:
            return False
    return True


if __name__ == "__main__":
    data1_path = os.path.abspath(
        r'G:\scores\beautiful\bin\{}\data_batch_0{}'.format(mode, '_480_440'))
    data2_path = os.path.abspath(
        r'G:\scores\beautiful\bin\{}\data_batch_0{}'.format(mode, '_480_640'))
    dict1 = unpickled(data1_path)
    # print(len(dict1['data']))
    # print(len(dict1['data'][0]))
    dict2 = unpickled(data2_path)
    print(compare(dict1['data'][0], dict2['data'][0]))
