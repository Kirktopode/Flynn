import sys
try:
    from bme280 import readBME280All
    import csv
    import math
    import lcd_16x2 as LCD
    from mpu6050 import mpu6050
    import os
    from os import listdir
    from os.path import isfile, join
    import smbus
    import time

    mpu = mpu6050(0x68)
    bus = smbus.SMBus(1)
    nano_address = 0x04
    LCD.lcd_init()
    def write_nano(value):
        bus.write_byte(nano_address, value)
        return -1

    def read_nano():
        number = bus.read_byte(nano_address)
        return number

    def get_altitude(pressure, baseline=1013.25):
        return 44330.0 * (1.0 - (pressure / baseline)**(1.0 / 5.255))


    mydir = "/".join(os.path.abspath(__file__).split("/")[:-1])
    logfiles = [f for f in listdir(mydir + "/logs") if isfile(join(mydir + "/logs", f))]
    count = 0
    while "log" + str(count) + ".csv" in logfiles:
        count += 1
    logfile = mydir + "/logs/log" + str(count) + ".csv"
    print(logfile)

    nanonum = 0
    t = 0
    baseline_p = 0
    for i in range(50):
        temp, p, h = readBME280All()
        baseline_p += p

    baseline_p /= 50

    print ('a["x"], a["y"], a["z"], g["x"], g["y"], g["z"], temp, p, nanonum, t, yaw, pitch, roll, altitude(relative), altitude(sea level)')
    with open(logfile, "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(['a["x"]', 'a["y"]', 'a["z"]', 'g["x"]', 'g["y"]', 'g["z"]', 'temp', 'p', nanonum, 't', 'yaw','pitch','roll', 'altitude(relative)', 'altitude(sea level)'])
        csvfile.close()
    while True:
        with open(logfile, "a") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",")
            try:
                a = mpu.get_accel_data(True)
            except:
                a = {"x":-999, "y":-999, "z":-999}
            try:
                g = mpu.get_gyro_data()
            except:
                g = {"x":-999, "y":-999, "z":-999}
            try:
                temp = 0
                p = 0
                h = 0
		for i in range(10):
                    temp_i, p_i, h_i = readBME280All()
                    temp += temp_i
                    p += p_i
                    h += h_i
                temp /= 10
                p /= 10
                h /= 10
            except:
                temp = -999
                p = -999
                h = -999
            try:
                write_nano(nanonum)
                if read_nano() == nanonum: nanonum += 1
            except:
                print("error")
            # sleep one second
            pitch =  math.degrees(math.atan2(a["y"], a["z"]))
            roll = math.degrees(math.atan2(-a["x"], a["z"]))
            yaw = g["z"]
            alt = get_altitude(p)
            alt_rel = get_altitude(p, baseline_p)
            LCD.lcd_string("Rel. Altitude",LCD.LCD_LINE_1)
            LCD.lcd_string("%.2f" % (alt_rel),LCD.LCD_LINE_2)
            csvwriter.writerow([a["x"], a["y"], a["z"], g["x"], g["y"], g["z"], temp, p, nanonum, t, yaw, pitch, roll, alt_rel, alt])
            print (a["x"], a["y"], a["z"], g["x"], g["y"], g["z"], temp, p, nanonum, t, yaw, pitch, roll, alt_rel, alt)
            csvfile.close()
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print(exc_type, exc_obj, exc_tb.tb_lineno)
