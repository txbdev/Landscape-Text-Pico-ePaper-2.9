from epd_2in9 import EPD_2in9
from centerwriter import CenterWriter
from rtc_ds3231 import ds3231
from utime import sleep
import myroboto
import gc

rtc = ds3231(1, 7, 6)
#rtc.set_time('15:46:30,Thursday,2023-04-13')

if __name__=='__main__':
    
    while True:
        rtc.read_time()
        
        inithr = rtc.hour()
        if inithr > 12:
            newhr = inithr-12
            ampm = "PM"
        elif inithr == 0:
            newhr = 12
            ampm = "AM"
        else:
            newhr = inithr
            ampm = "AM"
        
        hour = str(newhr)
        
        initmin = rtc.minute()
        if initmin < 10:
            minutes = "0"+str(initmin)
        else:
            minutes = str(initmin) 
        
        epd = EPD_2in9()
        epd.Clear(0xff)
        epd.fill(0xff)
        
        cw = CenterWriter(epd, myroboto)
        
        cw.set_vertical_spacing(0)
        cw.set_vertical_shift(0)
        cw.write_lines([hour+":"+minutes+" "+ampm])
        
        epd.display(epd.buffer)
        
        gc.collect()
        sleep(55)