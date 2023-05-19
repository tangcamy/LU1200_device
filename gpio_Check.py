# -*- coding: utf-8 -*-
"""
Created on Fri May 27 11:24:21 2022

@author: User
"""

# In[def]
def OUT_GPIO_Value(OUT_pin5,OUT_pin4,OUT_pin3,OUT_pin2,OUT_pin1,OUT_pin0,TYPE):
    #二進制-2**3(pin3),2**2(pin2),2**1(pin1),2**0(pin0)
    v_pin3=8*OUT_pin3
    v_pin2=4*OUT_pin2
    v_pin1=2*OUT_pin1
    v_pin0=1*OUT_pin0
    #二進制-2**3(x),2**2(x),2**1(pin5),2**0(pin4) 
    v_pin5=2*OUT_pin5
    v_pin4=1*OUT_pin4
    #得出結果
    f1=hex(v_pin0+v_pin1+v_pin2+v_pin3)
    f2=hex(v_pin4+v_pin5)
    try:
        f1=f1.split('0x')[1].upper()
        f2=f2.split('0x')[1].upper()
    except:
        f1=f1.split('0x')[1]
        f2=f2.split('0x')[1]
    final=str('0x00')+str(f2)+str(f1)
    if TYPE==True:
        if OUT_pin5==1:
            print('腳位OUT_5:ON')
        else:
            print('腳位OUT_5:OFF')
        if OUT_pin4==1:
            print('腳OUT_4:ON')
        else:
            print('腳位OUT_4:OFF')
        if OUT_pin3==1:
            print('腳位OUT_3:ON')
        else:
            print('腳位OUT_3:OFF')
        if OUT_pin2==1:
            print('腳位OUT_2:ON')
        else:
            print('腳位OUT_5:OFF')
        if OUT_pin1==1:
            print('腳位OUT_1:ON')
        else:
            print('腳位OUT_1:OFF')
        if OUT_pin0==1:
            print('腳位OUT_0:ON')
        else:
            print('腳位OUT_0:OFF')
    return final

def IN_GPIO_Value(IN_pin3,IN_pin2,IN_pin1,IN_pin0,TYPE):
    #二進制-2**3(X),2**2(X),2**1(pin3),2**0(pin2)
    v_pin3=2*IN_pin3
    v_pin2=1*IN_pin2
    #二進制-2**3(pin1),2**2(pin0),2**1(X),2**0(X) 
    v_pin1=8*IN_pin1
    v_pin0=4*IN_pin0
    #得出結果
    f1=hex(v_pin3+v_pin2)
    f2=hex(v_pin1+v_pin0)
    try:
        f1=f1.split('0x')[1].upper()
        f2=f2.split('0x')[1].upper()
    except:
        f1=f1.split('0x')[1]
        f2=f2.split('0x')[1]
    final=str('0x0')+str(f1)+str(f2)+'0'
    if TYPE==True:
        if IN_pin3==1:
            print('腳位IN_3:ON')
        else:
            print('腳位IN_3:OFF')
        if IN_pin2==1:
            print('腳位IN_2:ON')
        else:
            print('腳位IN_2:OFF')
        if IN_pin1==1:
            print('腳位IN_1:ON')
        else:
            print('腳位IN_1:OFF')
        if IN_pin0==1:
            print('腳位IN_0:ON')
        else:
            print('腳位IN_0:OFF')
    return final

def checkIn(valueconnect):             
    if valueconnect=='0380':
        showtype='IN_0:收到訊號'
    elif valueconnect=='0340':
        showtype='IN_1:收到訊號'
    elif valueconnect=='02C0':
        showtype='IN_2:收到訊號'
    elif valueconnect=='01C0':
        showtype='IN_3:收到訊號'
    else:
        showtype='未收到訊號_'+str(valueconnect)
    return showtype

