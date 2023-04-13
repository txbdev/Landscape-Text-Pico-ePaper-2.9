from machine import Pin, I2C
import time
import binascii

#    the first version use i2c1
I2C_PORT = 1
I2C_SDA = 6
I2C_SCL = 7

#    the new version use i2c0,if it dont work,try to uncomment the line 14 and comment line 17
#    it should solder the R3 with 0R resistor if want to use alarm function,please refer to the Sch file on waveshare Pico-RTC-DS3231 wiki
#    https://www.waveshare.net/w/upload/0/08/Pico-RTC-DS3231_Sch.pdf
# I2C_PORT = 0
# I2C_SDA = 20
# I2C_SCL = 21

class ds3231(object):
#  the register value is the binary-coded decimal (BCD) format
#               sec min hour week day month year
    NowTime = b'\x00\x45\x13\x02\x24\x05\x21'
    w  = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    address = 0x68
    start_reg = 0x00
    alarm1_reg = 0x07
    control_reg = 0x0e
    status_reg = 0x0f
    
    def __init__(self,i2c_port,i2c_scl,i2c_sda):
        self.bus = I2C(i2c_port,scl=Pin(i2c_scl),sda=Pin(i2c_sda))

    def set_time(self,new_time):
        hour = new_time[0] + new_time[1]
        minute = new_time[3] + new_time[4]
        second = new_time[6] + new_time[7]
        week = "0" + str(self.w.index(new_time.split(",",2)[1])+1)
        year = new_time.split(",",2)[2][2] + new_time.split(",",2)[2][3]
        month = new_time.split(",",2)[2][5] + new_time.split(",",2)[2][6]
        day = new_time.split(",",2)[2][8] + new_time.split(",",2)[2][9]
        now_time = binascii.unhexlify((second + " " + minute + " " + hour + " " + week + " " + day + " " + month + " " + year).replace(' ',''))
        #print(binascii.unhexlify((second + " " + minute + " " + hour + " " + week + " " + day + " " + month + " " + year).replace(' ','')))
        #print(self.NowTime)
        self.bus.writeto_mem(int(self.address),int(self.start_reg),now_time)
    
    def read_time(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        a = t[0]&0x7F  #second
        b = t[1]&0x7F  #minute
        c = t[2]&0x3F  #hour
        d = t[3]&0x07  #week
        e = t[4]&0x3F  #day
        f = t[5]&0x1F  #month
        
    def year(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[6]&0x70)/16) * 10
        lo = t[6]&0x0F
        return hi + lo
        
    def sec(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[0]&0x70)/16) * 10
        lo = t[0]&0x0F
        return hi + lo
    
    def minute(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[1]&0x70)/16) * 10
        lo = t[1]&0x0F
        return hi + lo
    
    def hour(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[2]&0x30)/16) * 10
        lo = t[2]&0x0F
        return hi + lo
    
    def week(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        lo = t[3]&0x07
        return lo
    
    def day(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[4]&0x30)/16) * 10
        lo = t[4]&0x0F
        return hi + lo
    
    def month(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[5]&0x10)/16) * 10
        lo = t[5]&0x0F
        return hi + lo
    
    def day_name(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        return(self.w[t[3]-1])
    
    