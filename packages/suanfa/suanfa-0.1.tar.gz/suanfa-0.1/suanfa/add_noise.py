import random
import numpy as np
def add_noise(img,noisecount=1000):
    h,w=img.shape[:2]
    new=np.array(img)
    for k in range(0,noisecount):
        xi=random.randint(0,w-1)
        xj=random.randint(0,h-1)
        new[xj,xi]=255
    return new

##img=cv.imread('lena.jpg',0)
##
##newing=add_noise(img)
##result=newing
###逐一像素点计算
##h,w=img.shape[:2]
##for i in range(1,h):
##    for j in range(1,w):
##        result[i,j]=(np.sum(newing[i-1:i+2,j-1:j+2]))/9
###2D滤波器
##k=np.ones((3,3),np.float32)/8
##dst=cv.filter2D(newing,-1,k)
###blur函数滤波
##re=cv.blur(newing,(3,3))
###合并图片以方便显示
##res1=np.hstack((newing,result))
##res2=np.hstack((dst,re))
###显示
##cv.imshow('12',res1)
##cv.imshow('34',res2)

#22、中值滤波
def paixu(a):
    b=[]
    for i in range(len(a)):
        m=max(a)
        b.append(m)
        a.remove(m)
    return b
def median(a):
    b=paixu(a)
    n=int(len(b)/2)
#    print(a,n)
    return b[n]
def twotoone(c):
    a=[n for a in c for n in a]
    return a
##img=cv.imread('lena.jpg',0)
##newing=add_noise(img)
###opencv自带函数medianBlur实现中值滤波
##res=cv.medianBlur(newing,3)
####cv.imshow('noisemap',newing)
####cv.imshow('result',res)
###逐个像素计算
##result=np.array(img)
##h,w=img.shape[:2]
##for i in range(1,h-2):
##    for j in range(1,w-2):
##        a=twotoone(newing[i-1:i+2,j-1:j+2])
##        n=median(a)
##        result[i,j]=n
##res1=np.hstack((newing,res,result))
##cv.imshow('median',res1)