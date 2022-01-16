from configparser import Interpolation
import os
from turtle import width
from PIL import Image
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import Workbook
import xlwt
def saveExcelData(bianhao,area1,area2):
   wb = xlwt.Workbook()
   ws = wb.add_sheet('1')
   for i  in range(len(bianhao)):
      ws.write(i,1,bianhao[i])
      ws.write(i,2,area1[i])
      ws.write(i,3,area2[i])
   wb.save('1.xlsx')



path = os.path.abspath(os.path.dirname(__file__))       # 这个文件所在的文件夹路径
pic_folder = os.path.join(path,"./camera")

imgs = glob.glob(os.path.join(pic_folder,"*"))  
bianhao = []
area1max = []
area2max = []
for img in imgs:
   a = img.split('\\')[-1].split('.')[0]
   bianhao.append(a[0])
   avg  = []
   
   area1 = []
   area2 = []
   area1_rows = 0
   area2_rows = 0
   image = cv2.imread(img)
   image = cv2.resize(image,(0,0),fx=0.5,fy=0.5)
   (height,width) = image.shape[:2]
   print((height,width))
   #切含有区域1和区域2的图
   x_start = int(width*0.46)
   x_end = int(width*0.6)
   y_start = int(height*0.53)
   y_end = int(height* 0.95)
   crop = image[y_start:y_end,x_start:x_end]
   # cv2.imshow('crop',crop)
   crop_h,crop_w = crop.shape[:2]
   print((crop_w,crop_h))
   for i in range(0,crop_h):
      row_gray_total = 0
      for j in range(0,crop_w):
         (b,g,r) = crop[i,j]
         gray = (int(r)+int(g)+int(b))*1.0/3.0
         row_gray_total += gray
      # avg.append(int(row_gray_total/width)-((height-i)*(20.0/height)))
      avg.append(row_gray_total/crop_w)
      # # 如果这行的平均灰度大于等于57的话，整行算进区域荧光面积
      if i <(crop_h/2):
         area1.append(row_gray_total/crop_w)
            # area1_rows+=1
            # total1 += (row_gray_total/width)
            # print("第%d行被计入区域1,平均灰度%d"%(i,row_gray_total/width))
      else:
         area2.append(row_gray_total/crop_w)
         # area2_rows+=1
            # total2 += (row_gray_total/width)
            # print("第%d行被计入区域2,平均灰度%d"%(i,row_gray_total/width))
      # print("区域1行数%d,区域2行数%d"%(area1_rows,area2_rows))
      # total1 = total1-min_avg_gray*area1_rows
      # total2 = total2-min_avg_gray*area2_rows
      # print("区域1的面积：%d 区域2的面积：%d"%(total1,total2))
   area1max.append(max(area1))
   area2max.append(max(area2))
   print("面积1最大值：%d 面积2最大值%d"%(max(area1),max(area2)))
   # x=np.arange(0,len(avg))+1
   # # print(avg)
   # # print(x)
   # x[0]=1
   # plt.rcParams['font.sans-serif']=['SimHei']
   # plt.title(img)
   # plt.xlabel("试剂位置（像素)")
   # plt.ylabel("平均灰度")
   # plt.plot(x,avg,label='list1',color='g',linewidth=2,linestyle=':')
   # plt.legend()
   # plt.show()

saveExcelData(bianhao,area1max,area2max)

#计算每一张的平均灰度
#存进数组
#for循环完成之后，写进excel里面
