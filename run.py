#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 17:01:45 2020
@author: ml5c01
"""
# In[import] 
import cv2
import datetime
import pandas as pd
import os 
import time
import threading
import numpy as np
#usb io
from ctypes import *
import platform
from time import sleep
from usb_device import *
from usb2gpio import *
from gpio_Check import *
# In[root]
current=os.getcwd()
imageroot=current+os.sep+'image'+os.sep
os.chdir(current)
#os.sep
# In[config]
CameraUrl=0#Baseconfig['setting']['cameraurl']
Camera_width=640#int(Baseconfig['setting']['cmaerawidth'])
# In[def]
def makedirs(path):#建立路徑
    try:
        os.makedirs(path)
    except:
        return
    
class Capture():#camera capture#QThread
    def __init__(self, URL):
        super(Capture,self).__init__()
        self.Frame = []
        self.status = False
        self.isstop = False	
	# 攝影機連接。
        self.capture = cv2.VideoCapture(URL)
        self.capture.set(3,Camera_width)# 寬度
        #self.capture.set(4,270)#      
    def start(self):
	# 把程式放進子執行緒，daemon=True 表示該執行緒會隨著主執行緒關閉而關閉。
        print('camera started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()
    def start_foronline(self):#上線使用
        print('camera started!')
        threading.Thread(target=self.queryframe_foronline, daemon=True, args=()).start()        
    def stop(self):
	# 記得要設計停止無限迴圈的開關。
        self.isstop = True
        isstop='Camera stopped'
        print('camera stopped!')
        self.capture.release()
        return isstop
    def getframe(self):
	# 當有需要影像時，再回傳最新的影像。
        return self.Frame        
    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()
        self.capture.release()
def Dic_saveimg(dicimg):
    for im in dicimg:
        image=dicimg[im]
        cv2.imwrite(imageroot+str(day)+os.sep+im,image)
        print(imageroot+str(day)+os.sep+im)
    fortest=['NG']
#    fortest=['OK']
    return fortest

makedirs(imageroot)
# In[run]
 #連接攝影機
camera_video = Capture(int(CameraUrl))         
# 啟動子執行緒
camera_video.start()
# 暫停1秒，確保影像已經填充
time.sleep(1)  

# In[usb device check]

print('------------PC電腦是否偵測到裝置--------------------')
DevHandles = (c_int * 20)()
DevHandle = 0
# Scan device
ret = USB_ScanDevice(byref(DevHandles))
if(ret == 0):
    print("No device connected!")
    exit()
else:
    print("Have %d device connected!"%ret)
    DevHandle = DevHandles[0]#选择设备0
# Open device
ret = USB_OpenDevice(DevHandle)
if(bool(ret)):
    print("Open device success!")
else:
    print("Open device faild!")
    exit()

# In[inline]
dic={}
nus=0
capture_time=0.1
delay_time=2
run_time=20
sleeptime=True
date = datetime.datetime.now()
#IN_value_connect='0340'
print('------------------IN/OUT 開啟設定---------------------')
in_pinmask=IN_GPIO_Value(1,1,1,1,True)
out_pinmask=OUT_GPIO_Value(1,1,1,1,1,1,True)
while True:
    GPIO_Write(DevHandle,0x003F,0x0000)
    try:
    #    save=None
        print('waitting...')
        day=date.strftime('%Y%m%d') #完整日期_上線 
        #--usb io test--#
        PinValue = c_uint(0)
        GPIO_Read(DevHandle,0x03C0,byref(PinValue))
        #print("READ DATA(Float):%04X"%PinValue.value)
        IN_value_connect="%04X"%PinValue.value
        print(checkIn(IN_value_connect))   
        if IN_value_connect=='0340':#IN_1
            end = datetime.datetime.now()
            if sleeptime==True:
                print('start delytime')
                time.sleep(delay_time)#delay time
                sleeptime=False
                date = datetime.datetime.now()
                end = datetime.datetime.now()            
            if (end-date).seconds <= run_time:
                print('---save dic---'+str((end-date).seconds))
                makedirs(imageroot+str(day))
                
                fileday=date.strftime('%Y%m%d_%H%M%S') #完整日期_上線 
                filename=fileday+'_'+str(nus)+'.jpg'
                #print(filename)  
                #使用無窮迴圈擷取影像，直到按下Esc鍵結束               
                I = camera_video.getframe()
                dic[filename]=I
                time.sleep(capture_time)#capture time
                nus=nus+1
    #           print(str(nus))      
        else:
            
            date = datetime.datetime.now()
            if len(dic)>0:
                answer=Dic_saveimg(dic)#改mura(dic)
                if 'NG' in answer:
                    #測試輸出訊號-後續要看判斷式調整-#
                    print('------------------OUT 開啟設定---------------------')
                    out_pinmask=OUT_GPIO_Value(1,1,1,1,1,1,True)#pin5,pin4,pin3,pin2,pin1,pin0
                #    print('------------------填寫數值---------------------')
                #    print('Gpio_SetOutput,GPIO_Write,GPIO_Read的第二欄位填寫:'+str(out_pinmask))
                    GPIO_SetOutput(DevHandle,0x003F,0) #0x003F
                     #2.-寫入啟動訊號,將要給予訊號的PIN給1
                    print('------------------寫入OUT訊號---------------------')
                #    out_control=OUT_GPIO_Value(0,0,0,0,1,0,True)#pin5,pin4,pin3,pin2,pin1,pin0
                #    print('Gpio_Write第三欄位填寫:'+str(out_control))
                    GPIO_Write(DevHandle,0x003F,0x0002)
                    time.sleep(1)
                else:
                    #測試輸出訊號-後續要看判斷式調整-#
                    print('------------------OUT 開啟設定---------------------')
                    out_pinmask=OUT_GPIO_Value(1,1,1,1,1,1,True)#pin5,pin4,pin3,pin2,pin1,pin0
                #    print('------------------填寫數值---------------------')
                #    print('Gpio_SetOutput,GPIO_Write,GPIO_Read的第二欄位填寫:'+str(out_pinmask))
                    GPIO_SetOutput(DevHandle,0x003F,0) #0x003F
                     #2.-寫入啟動訊號,將要給予訊號的PIN給1
                    print('------------------寫入OUT訊號---------------------')
                #    out_control=OUT_GPIO_Value(0,0,0,0,1,0,True)#pin5,pin4,pin3,pin2,pin1,pin0
                #    print('Gpio_Write第三欄位填寫:'+str(out_control))
                    GPIO_Write(DevHandle,0x003F,0x0000)
                dic={}
                nus=0
                sleeptime=True
            else:
                dic={}
                nus=0
                sleeptime=True
    except:
        print('camera disconnect')
            

    
