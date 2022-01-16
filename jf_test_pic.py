import cv2
import numpy as np
import glob
from PIL import Image
import pandas as pd
from PIL import ImageStat
import matplotlib.pyplot as plt

## 色调（H），饱和度（S），明度（V）
import os

def calculation(gray_list):
    #拉开高值和低值的差距，能有个100倍就可以了
    #获取最高灰度值和最低灰度值,然后这个系数的平方值*灰度值
    level_more_250 = 100
    level_200_250 =50
    level_100_200 = 25
    levle_50_100 = 10

   
    xishu = 2
    temp = []
    for i in gray_list:
     
        if i >=254:
            i = i* level_more_250
        elif i>=253:
            i = i* (level_more_250-10)
        elif i>=252:
            i = i* (level_more_250-20)
        elif i>= 251:
            i = i* (level_more_250-30)
        elif i>= 250:
            i = i* (level_more_250-40)
        #如果小于250,且大于100的话，全部当做是中值区域来计算
        elif i>=200 and i<250:
            i = i*(level_200_250-(250-i)*0.5)
        elif i< 200 and i>=100:
            i = i*(level_100_200-(200-i)*0.15)
        elif i<100 and i>50:
            i = i*(levle_50_100-(100-i)*0.1)
        temp.append(i)        
    print("拉开后的平均灰度是：",temp)
    return temp


path = os.path.abspath(os.path.dirname(__file__))       # 这个文件所在的文件夹路径
pic_folder = os.path.join(path,"./2")
# liangdulist = []
# baohedu  = []
# sediao = []
pathlist = []
imgs = glob.glob(os.path.join(pic_folder,"5*"))      # 将所有的符合这个后缀名的文件存到一个列表并返回这个列表

area1 = []
area2 = []

for imgpath in imgs:
    pixels = 0
    total = 0
    min_avg_gray = 70
    print("-----------------")
    print(imgpath)
    a = imgpath.split('\\')[-1].split('.')[0]
    pathlist.append(a)
    #image = cv2.imread(imgpath)
    #image = cv2.imdecode(np.fromfile(imgpath,dtype=np.uint8),cv2.IMREAD_COLOR)        # 含有中文名字的读取方法
    img0 = cv2.imdecode(np.fromfile(imgpath,dtype=np.uint8),1)
    gray = cv2.cvtColor(img0,cv2.COLOR_RGB2GRAY)
    # H,S,V = cv2.split(hsv)

    height,width,mode = img0.shape
    print("图片高度%d,宽度%d"%(height,width))
    pixels = height*width
    row_area = [] #行面积
    total1 = 0
    total2 = 0
    avg = []
    area2 = []
    y = []
    area1_rows= 0
    area2_rows = 0
    #遍历所有的行，平均灰度小于57的不要了
    for i in range(0,height):
        row_gray_total = 0
        for j in range(0,width):
            (b,g,r) = img0[i,j]
            gray = (int(r)+int(g)+int(b))*1.0/3.0
            row_gray_total += gray
        # avg.append(int(row_gray_total/width)-((height-i)*(20.0/height)))
        avg.append(int(row_gray_total/width))

        #如果这行的平均灰度大于等于57的话，整行算进区域荧光面积
        if (row_gray_total/width)>=min_avg_gray :
            if i <(height/2):
                
                area1_rows+=1
                total1 += (row_gray_total/width)
                # print("第%d行被计入区域1,平均灰度%d"%(i,row_gray_total/width))
            else:
                area2_rows+=1
                total2 += (row_gray_total/width)
                        # print("第%d行被计入区域2,平均灰度%d"%(i,row_gray_total/width))
    print("区域1行数%d,区域2行数%d"%(area1_rows,area2_rows))
    total1 = total1-min_avg_gray*area1_rows
    total2 = total2-min_avg_gray*area2_rows
    print("区域1的面积：%d 区域2的面积：%d"%(total1,total2))
    # avg.append(total1/total2)
    # result = calculation(avg)

x=np.arange(0,len(avg))+1
# print(avg)
# print(x)
x[0]=1
plt.rcParams['font.sans-serif']=['SimHei']
plt.title(a)
plt.xlabel("试剂位置（像素)")
plt.ylabel("平均灰度")
# plt.subplot(1,2,1)
# plt.plot(x,result,label='list1',color='g',linewidth=2,linestyle=':')
# plt.axhline(min(result), color='r', linestyle='--', label='Y')

# plt.subplot(1,2,2)
plt.plot(x,avg,label='list1',color='g',linewidth=2,linestyle=':')


plt.legend()
plt.show()


# excel = pd.DataFrame(avg)
# excel.to_excel("area.xls")
# excel = pd.DataFrame(liangdulist)
# excel.to_excel("liangdu_20211122.xls")
# excel = pd.DataFrame(sediao)
# excel.to_excel("sediao_20211122.xls")
# excel = pd.DataFrame(x)
# excel.to_excel("bianhao.xls")