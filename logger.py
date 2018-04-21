from bme280 import readBME280All
from mpu6050 import mpu6050

import os
import sys
import csv
import smbus
import time

mpu = mpu6050()
bus = smbus.SMBus(1)
nano_address = 0x04

def write_nano(value):
    bus.write_byte(address, value)
    return -1

def read_nano():
    number = bus.read_byte(address)
    return number

while True:

    writeNumber(var)
    print ("RPI: Hi Arduino, I sent you", var)
    # sleep one second
    time.sleep(1)

    number = readNumber()
    print ()
