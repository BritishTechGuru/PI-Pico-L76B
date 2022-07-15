# -*- coding:utf-8 -*-

import time
import l76x
import time
import math

'''
uart_print = UART(0,baudrate=9600,tx=Pin(0),rx=Pin(1))
#uart_print = UART(1,baudrate=9600,tx=Pin(4),rx=Pin(5))
StandBy = Pin(17,Pin.OUT)
StandBy.value(0)
ForceOn = Pin(14,Pin.OUT)
ForceOn.value(0)
rxData = bytes()

while True:
    while uart_print.any() > 0:
        rxData += uart_print.read(1)
    print(rxData.decode('utf-8'))
'''

x=l76x.L76X()
x.L76X_Set_Baudrate(9600)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)
x.L76X_Set_Baudrate(115200)

x.L76X_Send_Command(x.SET_POS_FIX_400MS);

#Set output message
x.L76X_Send_Command(x.SET_NMEA_OUTPUT);

time.sleep(2)
x.L76X_Exit_BackupMode();
x.L76X_Send_Command(x.SET_SYNC_PPS_NMEA_ON)

#x.L76X_Send_Command(x.SET_STANDBY_MODE)
#time.sleep(10)
#x.L76X_Send_Command(x.SET_NORMAL_MODE)
#x.config.StandBy.value(1)

while(1):
    
    RSTime, RSLattitude, RSLongtitude, RSGroundSpeed, RSDirection, RSDate, RSVariation = x.L76X_Gat_GNRMC()

    print ("Time : ", RSTime)
    print ("Lattitude : ", RSLattitude)
    print ("Longtitude : ", RSLongtitude)
    print ("Ground speed in knots : ", RSGroundSpeed)
    print ("Compass direction : ", RSDirection)
    print ("Today's date : ", RSDate)
    print ("Magnetic Variation : ", RSVariation)
    print ("--------------------------------------------")

    time.sleep(5)


