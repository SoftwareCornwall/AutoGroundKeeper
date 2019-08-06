# -*- coding: utf-8 -*-
import pump_control
import time

def main():
    pump = pump_control.Pump()  
    for _ in range(8):
        pump.enable_pump_for_duration(2)
        time.sleep(3 * 3600)
        
if __name__ == '__main__':
    main()
