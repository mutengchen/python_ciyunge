#读取每一个图片，截取里面的某一块的区域
import cv2
import numpy as np
import glob
from PIL import Image
import pandas as pd
from PIL import ImageStat
## 色调（H），饱和度（S），明度（V）
import os

path = os.path.abspath(os.path.dirname(__file__))
pic_folder = os.path.join(path,"./jf_test")
imgs = glob.glob(os.path.join(pic_folder,"*.jpg"))

pixels = 3000
for imgpath in imgs:
    print("-----------------")
    print(imgpath)
    image = cv2.imread(imgpath)
    cropImg = image[440:670,940:990]
    cv2.imwrite("resize_"+imgpath.split('\\')[-1],cropImg)
