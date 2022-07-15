# -*- coding:utf-8 -*-

from machine import Pin
import l76_config
import math
import time

Temp = '0123456789ABCDEF*'
BUFFSIZE = 1100

pi = 3.14159265358979324
a = 6378245.0
ee = 0.00669342162296594323
x_pi = 3.14159265358979324 * 3000.0 / 180.0

class L76X(object):
    Lon = 0.0
    Lat = 0.0
    Lon_area = 'E'
    Lat_area = 'W'
    Time_H = 0
    Time_M = 0
    Time_S = 0
    Status = 0
    Lon_Baidu = 0.0
    Lat_Baidu = 0.0
    Lon_Google = 0.0
    Lat_Google = 0.0
    
    GPS_Lon = 0
    GPS_Lat = 0
    
    GPS_Speed = 0
    GPS_Direction = 0
    GPS_DATA = ""
    
    #Startup mode
    SET_HOT_START       = '$PMTK101'
    SET_WARM_START      = '$PMTK102'
    SET_COLD_START      = '$PMTK103'
    SET_FULL_COLD_START = '$PMTK104'

    #Standby mode -- Exit requires high level trigger
    SET_PERPETUAL_STANDBY_MODE      = '$PMTK161'
    SET_STANDBY_MODE                = '$PMTK161,0'

    SET_PERIODIC_MODE               = '$PMTK225'
    SET_NORMAL_MODE                 = '$PMTK225,0'
    SET_PERIODIC_BACKUP_MODE        = '$PMTK225,1,1000,2000'
    SET_PERIODIC_STANDBY_MODE       = '$PMTK225,2,1000,2000'
    SET_PERPETUAL_BACKUP_MODE       = '$PMTK225,4'
    SET_ALWAYSLOCATE_STANDBY_MODE   = '$PMTK225,8'
    SET_ALWAYSLOCATE_BACKUP_MODE    = '$PMTK225,9'

    #Set the message interval,100ms~10000ms
    SET_POS_FIX         = '$PMTK220'
    SET_POS_FIX_100MS   = '$PMTK220,100'
    SET_POS_FIX_200MS   = '$PMTK220,200'
    SET_POS_FIX_400MS   = '$PMTK220,400'
    SET_POS_FIX_800MS   = '$PMTK220,800'
    SET_POS_FIX_1S      = '$PMTK220,1000'
    SET_POS_FIX_2S      = '$PMTK220,2000'
    SET_POS_FIX_4S      = '$PMTK220,4000'
    SET_POS_FIX_8S      = '$PMTK220,8000'
    SET_POS_FIX_10S     = '$PMTK220,10000'

    #Switching time output
    SET_SYNC_PPS_NMEA_OFF   = '$PMTK255,0'
    SET_SYNC_PPS_NMEA_ON    = '$PMTK255,1'

    #To restore the system default setting
    SET_REDUCTION               = '$PMTK314,-1'

    #Set NMEA sentence output frequencies 
    SET_NMEA_OUTPUT = '$PMTK314,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0'
    #Baud rate
    SET_NMEA_BAUDRATE          = '$PMTK251'
    SET_NMEA_BAUDRATE_115200   = '$PMTK251,115200'
    SET_NMEA_BAUDRATE_57600    = '$PMTK251,57600'
    SET_NMEA_BAUDRATE_38400    = '$PMTK251,38400'
    SET_NMEA_BAUDRATE_19200    = '$PMTK251,19200'
    SET_NMEA_BAUDRATE_14400    = '$PMTK251,14400'
    SET_NMEA_BAUDRATE_9600     = '$PMTK251,9600'
    SET_NMEA_BAUDRATE_4800     = '$PMTK251,4800'

    def __init__(self):
        self.config = l76_config.config(9600)
    
    def L76X_Send_Command(self, data):
        Check = ord(data[1]) 
        for i in range(2, len(data)):
            Check = Check ^ ord(data[i]) 
        data = data + Temp[16]
        data = data + Temp[int(Check/16)]
        data = data + Temp[int(Check%16)]
        self.config.Uart_SendString(data.encode())
        self.config.Uart_SendByte('\r'.encode())
        self.config.Uart_SendByte('\n'.encode())
        
    def L76X_Gat_GNRMC(self):
#we are only after the GNRMC field and only want:
# latitude, longtitude, direction, time and speed. Nothing else is of
# any importance - maybe data valid might be needed - don't yet know
        data = self.config.Uart_ReceiveString(BUFFSIZE)
        stringy = data.decode('UTF-8')
        StLen = len(stringy)
        if (stringy.find("$GNRMC") >-1):
#crop everything before the first field
            StartPoint = stringy.index("$GNRMC")+7
            stringy = stringy[StartPoint: (StLen - StartPoint)]    
#crop everything from the second $        
            EndPoint = stringy.index("$")
            stringy = stringy[0:EndPoint]
#now make it into a list
            Listy = stringy.split(',')
            RSTime = Listy[0]
            RSValid = Listy[1]
            RSLattitude = Listy[2]
            RSNSHemisphere = Listy[3]
            RSLongtitude = Listy[4]
            RSWEHemisphere = Listy[5]
            RSGroundSpeed = Listy[6]
            RSDirection = Listy[7]
            RSDate = Listy[8]
            RSVariation = Listy[9]
            RSChecksum = Listy[10]
#now return the required values to the program. That, for the drone operation will be
            return RSTime, RSLattitude, RSLongtitude, RSGroundSpeed, RSDirection, RSDate, RSVariation

            
    def L76X_Set_Baudrate(self, Baudrate):
        self.config.Uart_Set_Baudrate(Baudrate)

    def L76X_Exit_BackupMode(self):
        self.config.Force.value(1)
        time.sleep(1)
        self.config.Force.value(0)
        time.sleep(1)
        self.config.Force = Pin(self.config.FORCE_PIN,Pin.IN)
        

    
