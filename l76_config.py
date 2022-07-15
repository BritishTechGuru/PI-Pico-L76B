#!/usr/bin/python
# -*- coding:utf-8 -*-
from machine import UART,Pin

Temp = '0123456789ABCDEF*'

class config(object):
    FORCE_PIN  = 14
    STANDBY_PIN= 17
    def __init__(self, Baudrate = 9600):
        #self.ser = UART(1,baudrate=9600,tx=Pin(4),rx=Pin(5))
        self.ser = UART(0,baudrate=9600,tx=Pin(0),rx=Pin(1))
        self.StandBy = Pin(self.STANDBY_PIN,Pin.OUT)
        self.Force = Pin(self.FORCE_PIN,Pin.IN)
        self.StandBy.value(0)
        self.Force.value(0)

    def Uart_SendByte(self, value): 
        self.ser.write(value)
#        print("sendbyte")

    def Uart_SendString(self, value): 
        self.ser.write(value)
#        print("sendstring")

    def Uart_ReceiveByte(self):
#        print("receive byte")
        return self.ser.read(1)

    def Uart_ReceiveString(self, value): 
        data = self.ser.read(value)
#        print("receive string", data)
        return data

    def Uart_Set_Baudrate(self, Baudrate):
        self.ser = UART(0,baudrate=Baudrate,tx=Pin(0),rx=Pin(1))
