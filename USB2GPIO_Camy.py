# -*- coding: utf-8 -*-
"""
Created on Fri May 27 11:24:21 2022

@author: User
"""
from ctypes import *
import platform
from time import sleep
from usb_device import *
from usb2gpio import *
from gpio_Check import *
# In[check device]
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

# In[GPIO OUT Setting]
'''
#1.--設定哪些腳位為output (0:表示關閉，1表示開啟(高電位，設備燈不會亮))
print('------------------OUT 開啟設定---------------------')
out_pinmask=OUT_GPIO_Value(1,1,1,1,1,1,True)#pin5,pin4,pin3,pin2,pin1,pin0
print('------------------填寫數值---------------------')
print('Gpio_SetOutput,GPIO_Write,GPIO_Read的第二欄位填寫:'+str(out_pinmask))
GPIO_SetOutput(DevHandle,0x003F,0) #0x003F
 #2.-寫入啟動訊號,將要給予訊號的PIN給1
print('------------------寫入OUT訊號---------------------')
out_control=OUT_GPIO_Value(0,0,0,0,1,0,True)#pin5,pin4,pin3,pin2,pin1,pin0
print('Gpio_Write第三欄位填寫:'+str(out_control))
GPIO_Write(DevHandle,0x003F,0x0002) 
'''
#3.-確認輸出的高低電位
#print('------------------確認輸出訊號---------------------')
#PinValue = c_uint(0)
#check_read=GPIO_Read(DevHandle,0x003F,byref(PinValue))
##high&low
#OUT_value_connect=bin(PinValue.value)[2:]
#pin_start=5
#for i in range(0,len(OUT_value_connect)):
#    if pin_start>=0:
#        if str(OUT_value_connect[i]) =='1':
#            print('OUT_'+str(pin_start)+'電位為:HIGH')
#        else:
#            print('OUT_'+str(pin_start)+'電位為:LOW')
#        pin_start=pin_start-1    

# In[GPIO In Setting]

print('------------------IN 開啟設定---------------------')
in_pinmask=IN_GPIO_Value(1,1,1,1,True)
print('Gpio_SetInput第二欄位填寫:'+str(in_pinmask))
GPIO_SetInput(DevHandle,0x03C0,0)

while True:
    PinValue = c_uint(0)
    GPIO_Read(DevHandle,0x03C0,byref(PinValue))
    #print("READ DATA(Float):%04X"%PinValue.value)
    IN_value_connect="%04X"%PinValue.value
    print(checkIn(IN_value_connect))
    #sleep(5)


