import sys
try:
    from bme280 import readBME280All
    from mpu6050 import mpu6050
    import os
    from os import listdir
    from os.path import isfile, join
    import csv
    import smbus
    import time

    mpu = mpu6050(0x68)
    bus = smbus.SMBus(1)
    nano_address = 0x04

    def write_nano(value):
        bus.write_byte(nano_address, value)
        return -1

    def read_nano():
        number = bus.read_byte(nano_address)
        return number


    mydir = "/".join(os.path.abspath(__file__).split("/")[:-1])
    logfiles = [f for f in listdir(mydir + "/logs") if isfile(join(mydir + "/logs", f))]
    count = 0
    while "log" + str(count) + ".csv" in logfiles:
        count += 1
    logfile = mydir + "/logs/log" + str(count) + ".csv"
    print(logfile)
    
    nanonum = 0
    t = 0
    print ('a["x"], a["y"], a["z"], g["x"], g["y"], g["z"], temp, p, nanonum, t')
    with open(logfile, "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(['a["x"]', 'a["y"]', 'a["z"]', 'g["x"]', 'g["y"]', 'g["z"]', 'temp', 'p', nanonum, 't'])
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
                temp, p, h = readBME280All()
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
            time.sleep(0.5)
            t += 0.5
            csvwriter.writerow([a["x"], a["y"], a["z"], g["x"], g["y"], g["z"], temp, p, nanonum, t])
            print (a["x"], a["y"], a["z"], g["x"], g["y"], g["z"], temp, p, nanonum, t)
            csvfile.close()
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print(exc_type, exc_obj, exc_tb.tb_lineno)
