from HPT import HPT
from SCD41 import SCD41
import time, struct

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq = 10000)
hpt = HPT(i2c)
scd = SCD41(i2c)
print("periodic")

scd.periodic_measurement()
time.sleep(5)
while 1:
    if scd.data_ready_status():
        print(scd.read_measurement())
        time.sleep(5)



