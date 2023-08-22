import time, struct

class SCD41:
    
    square = (2 ** 16) - 1

    CRC8_POLYNOMIAL = 0x131
    crc_table = []
    for crc in range(256):
        for crc_bit in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ CRC8_POLYNOMIAL;
            else:
                crc = (crc << 1);
            crc = crc%256
        crc_table.append(crc)
    #print (crc_table)
        
    CRC_TABLE = crc_table
    
    def __init__(self, i2c):
        self.i2c = i2c
    
    def __crc(self, msb, lsb):
        crc = 0xff
        crc ^= msb
        crc = self.CRC_TABLE[crc]
        if lsb is not None:
            crc ^= lsb
            crc = self.CRC_TABLE[crc]
        return crc

    def check_crc(self, arr):
        if (len(arr) == 3):
            if self.__crc(arr[0], arr[1]) != arr[2]:
                value = False
            else:
                value = True
        else:
            value = False
        
        return value
    
    def send_command(self, command, value, wait = 0, size = 16):
        if value != None:
            bint = struct.pack('>H', value)
            msb = bint[0]
            lsb = bint[1]
            crc = 0xff
            crc ^= msb
            crc = self.CRC_TABLE[crc]
            if lsb is not None:
                crc ^= lsb
                crc = self.CRC_TABLE[crc]
            crch = crc
            data = bint + bytes([crch])
        else:
            data = b''
        
        self.i2c.writeto_mem(0x62, command, data, addrsize = size)
        time.sleep_ms(wait)
        
    def periodic_measurement(self, start = True, lowpower = False):
        if start:
            wait = 5000
            if lowpower:
                command = 0x21ac
            else:
                command = 0x21b1
        else:
            command = 0x3f86
            wait = 500
        self.send_command(command, 1, wait)
        
    def read_measurement(self):
        command = 0xec05
        self.send_command(command, None, 1)
        dataSCD = self.i2c.readfrom(0x62, 18)
        
        value = dataSCD[0:]
        crc = [value[0], value[1], value[2]]
        if self.check_crc(crc):
            co2 = (value[0] << 8) | value[1]
        else:
            co2 = -1
        
        value = dataSCD[3:]
        crc = [value[0], value[1], value[2]]
        if self.check_crc(crc):
            temp = (value[0] << 8) | value[1]
            temp = -45 + 175 * (temp / (2**16))
        else:
            temp = -1
        
        value = dataSCD[6:]
        crc = [value[0], value[1], value[2]]
        if self.check_crc(crc):
            rh = (value[0] << 8) | value[1]
            rh = 100 * (rh/(2**16))
        else:
            rh = -1
        
        return (round(temp, 2), round(rh, 2), round(co2, 0))
    
    def data_ready_status (self):
        command = 0xe4b8
        self.send_command(command, None, 1)
        dataSCD = self.i2c.readfrom(0x62, 3)
        ready = ((dataSCD[0] & 0x07 == 0))
        return ready
    
    def set_temperature_offset (self, offset):
        command = 0x241d
        bint = struct.pack('>H', int(offset * 100))
        crc = self.__crc(bint[0], bint[1])
        data = bint + bytes([crc])
        self.send_command(command, data, 1)
    
    def get_temperature_offset(self):
        command = 0x2318
        self.send_command(command, None, 1)
        dataSCD = self.i2c.readfrom(0x62, 3)
        self.__check_crc(dataSCD)
        return struct.unpack('>H', data.SCD)[0] / 100.0
    
    def set_sensor_altitude(self, altitude):
        command = 0x2427
        data = struct.pack('>H', altitude)
        crc = self.__crc(data[0], data[1])
        data = data + bytes([crc])
        self.send_command(command, data, 1)
    
    def get_sensor_altitude(self):
        command = 0x2322
        self.send_command(command, None, 1)
        dataSCD = self.i2c.readfrom(0x62, 3)
        self.__check_crc(dataSCD)
        return struct.unpack('>H', dataSCD)[0]
    
    def set_ambient_pressure(self, pressure):
        command = 0xe000
        pressure = pressure / 100
        data = struct.pack('>H', pressure)
        crc = self.__crc(data[0], data[1])
        data = data + bytes([crc])
        self.send_command(command, data, 1)
    
    def forced_recalibration(self, ppm):
        command = 0x362f
        data = int(ppm)
        self.send_command(command, data, 1)
        time.sleep_ms(400)
    
    def set_auto_self_calibration(self, data = 1):
        command = 0x2416
        self.send_command(command, data)
        
    def get_auto_self_calibration(self):
        command = 0x2313
        self.send_command(command, None, 1000)
        dataSCD = self.i2c.readfrom(0x62, 3)
        cal = (dataSCD[0] << 8) | dataSCD[1]
        return cal
    
    def persist_settings (self):
        command = 0x3682
        self.send_command(command, None, 800)
    
    def get_serial_number (self):
        command = 0x3682
        self.send_command(command, None, 1)
        dataSCD = self.i2c.readfrom(0x62, 9)
        serial = (dataSCD[0] << 32) + (dataSCD[1] << 16) + dataSCD[2]
        serial = tuple([(dataSCD[i] << 8) | dataSCD[i+1] for i in range(0, 9, 3)])
        return serial
    
    def self_test (self):
        command = 0x3639
        self.send_command(command, None, 10000)
        dataSCD = self.i2c.readfrom(0x62, 3)
        test = (dataSCD[0] << 8) + dataSCD[1]
        return test
    
    def factory_reset (self):
        command = 0x3632
        self.send_command(command, None, 1200)
    
    def reint (self):
        command = 0x3646
        self.send_command(command, None, 20)
    
    def measure_single_shot(self, RHT = False):
        if RHT:
            command = 0x2196
        else:
            command = 0x219d
        self.send_command(command, None, 5500)
        
        dataSCD = self.i2c.readfrom(0x62, 9)
        co2 = (dataSCD[0] << 8) | dataSCD[1]
        temp = (dataSCD[3] << 8) | dataSCD[4]
        rh = (dataSCD[6] << 8) | dataSCD[7]
        temp = -45 + 175 * (temp / (2**16))
        rh = 100 * (rh/(2**16))
        
        return (temp, rh, co2)  