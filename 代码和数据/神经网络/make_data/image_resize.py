import cv2 as cv
import numpy as np
import os

def image_resize(image_type, mode, size):
    src_path = r"G:\scores\{}\src\{}\480_300".format(image_type, mode)
    out_path = r"G:\scores\{}\src\{}\480_{:d}".format(image_type, mode, size)
    dirs = os.listdir(src_path)
    for f in dirs:
        filename = os.path.join(src_path, f)
        src = cv.imread(filename)
        dst = cv.resize(src, (480, size))
        res = cv.resize(dst, (480, 300))
        cv.imwrite(os.path.join(out_path, f), res)

if __name__ == "__main__":
    image_type = 'depressing'
    mode = 'test'
    image_resize(image_type, mode, 320)
    image_resize(image_type, mode, 440)
    image_resize(image_type, mode, 640)
