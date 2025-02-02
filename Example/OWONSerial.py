# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 09:00:38 2025

@author: gert
"""

#!/usr/bin/env python3
# MIT License

import serial
import argparse
from time import sleep
import time


from enum import Enum

class SCPICommand(Enum):
    # System Commands
    IDENTIFY = "*IDN?"
    REMOTE_MODE = "SYST:REM"
    LOCAL_MODE = "SYST:LOC"
    
    # Measurement Commands
    MEASURE = "MEAS?"
    MEASURE_VOLT = "MEAS:VOLT?"
    MEASURE_CURRENT = "MEAS:CURRENT?"
    
    MEASURE_1 = "MEAS1?"
    MEASURE_2 = "MEAS2?"
    MEASURE_SHOW = "MEAS:SHOW?"
    MEASURE_1_SHOW = "MEAS1:SHOW?"
    MEASURE_2_SHOW = "MEAS2:SHOW?"

    # Function Selection
    FUNCTION = "FUNC?"
    FUNCTION_1 = "FUNC1?"
    FUNCTION_2 = "FUNC2?"
    
    # Configuration Commands
    CONF_VOLT_DC_AUTO = "CONF:VOLT:DC AUTO"
    CONF_VOLT_DC = "CONF:VOLT:DC"
    CONF_VOLT_AC_AUTO = "CONF:VOLT:AC AUTO"
    CONF_CURR_DC_AUTO = "CONF:CURR:DC AUTO"
    CONF_CURR_DC = "CONF:CURR:DC"
    CONF_CURR_AC_AUTO = "CONF:CURR:AC AUTO"
    CONF_RES_AUTO = "CONF:RES AUTO"
    CONF_CAP_AUTO = "CONF:CAP AUTO"
    CONF_FREQ = "CONF:FREQ"
    CONF_PER = "CONF:PER"
    CONF_DIOD = "CONF:DIOD"
    CONF_CONT = "CONF:CONT"
    CONF_TEMP_RTD = "CONF:TEMP:RTD"

    # Temperature Settings
    TEMP_RTD_UNIT_C = "TEMP:RTD:UNIT C"
    TEMP_RTD_UNIT_F = "TEMP:RTD:UNIT F"
    TEMP_RTD_UNIT_K = "TEMP:RTD:UNIT K"
    TEMP_RTD_SHOW_TEMP = "TEMP:RTD:SHOW TEMP"
    TEMP_RTD_SHOW_MEAS = "TEMP:RTD:SHOW MEAS"
    TEMP_RTD_SHOW_ALL = "TEMP:RTD:SHOW ALL"

    # Beep Control
    BEEP_STATUS = "BEEP:STAT?"
    BEEP_ON = "BEEP:STAT ON"
    BEEP_OFF = "BEEP:STAT OFF"

    # Auto Range and Range Settings
    AUTO = "AUTO"
    AUTO_QUERY = "AUTO?"
    RANGE_SET = "RANGE"
    RANGE_QUERY = "RANGE?"

    # Measurement Speed
    RATE = "RATE"
    RATE_QUERY = "RATE?"
    
    # Continuity
    CONTINUITY_THRESHOLD = "CONT:THRE"
    
    # Math Functions
    CALC_FUNC = "CALC:FUNC"
    CALC_FUNC_QUERY = "CALC:FUNC?"
    CALC_DB_REF = "CALC:DB:REF"
    CALC_DB_REF_QUERY = "CALC:DB:REF?"
    CALC_DBM_REF = "CALC:DBM:REF"
    CALC_DBM_REF_QUERY = "CALC:DBM:REF?"
    CALC_AVERAGE_QUERY = "CALC:AVER:AVER?"
    CALC_MIN_QUERY = "CALC:AVER:MIN?"
    CALC_MAX_QUERY = "CALC:AVER:MAX?"
    CALC_OFF = "CALC:STAT OFF"

    # Reset (Not functional)
    RESET = "*RST"

class SCPI:
    """
    Serial SCPI interface
    """
    _SIF = None

    def __init__(self, port_dev=None, speed=9600, timeout=2):
        self._SIF = serial.Serial(
            port=port_dev,
            baudrate=speed,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=timeout
        )

    def __del__(self):
        try:
            self._SIF.close()
        except:
            pass

    def readdata(self):
        """
        Read a SCPI response terminated by CR LF.
        """
        buf = bytearray(0)
        while True:
            data = self._SIF.read(64)
            if len(data) > 0:
                buf.extend(data)
                if len(buf) >= 2 and buf[-2:] == b'\r\n':
                    break
            else:
                break
        return buf.decode(errors="backslashreplace").strip()

    def sendcmd(self, msg, getdata=True):
        """
        Send a SCPI command. If `getdata` is True, waits for a response.
        """
        msg = msg + '\n'
        self._SIF.write(msg.encode('ascii'))
        if getdata:
            return self.readdata()
        return None


def measure_voltage_current(device, duration, interval):
    """
    Measure voltage and current for the specified duration and interval.
    """
    print("Starting measurements...")
    print("Time (s), Voltage (V), Current (A)")

    elapsed_time = 0
    start_time = time.time()
    while elapsed_time < duration:
        try:
            # Measure voltage
            cycle_start = time.time()
            device.sendcmd(SCPICommand.CONF_VOLT_DC_AUTO.value)
            voltage = float(device.sendcmd(SCPICommand.MEASURE_VOLT.value).replace('V', ''))
            voltage = float(device.sendcmd(SCPICommand.MEASURE_VOLT.value).replace('V', ''))
            # Measure current
            device.sendcmd(SCPICommand.CONF_CURR_DC_AUTO.value)
            current = float(device.sendcmd(SCPICommand.MEASURE_CURRENT.value).replace('A', ''))
            current = float(device.sendcmd(SCPICommand.MEASURE_CURRENT.value).replace('A', ''))
            print(f"{elapsed_time:6.1f}, {voltage:9.5f}, {current:9.5f}")

        except Exception as e:
            print(f"Error during measurement: {e}")
        cycle_time = time.time() - cycle_start
        sleep_time = max(0, interval - cycle_time)
        sleep(sleep_time)
        elapsed_time += interval

    print("Measurements completed.")

def measure_a_voltage_and_current(device):
    """
    Measure voltage and current for the specified duration and interval.
    """
    try:
        # Measure voltage
        device.sendcmd("CONF:VOLT:DC AUTO")
        device.sendcmd(SCPICommand.CONFIG_VOLT_DC_AUTO.value)
        voltage = float(device.sendcmd(SCPICommand.MEASURE_VOLT.value).replace('V', ''))
        voltage = float(device.sendcmd(SCPICommand.MEASURE_VOLT.value).replace('V', ''))
        # Measure current
        device.sendcmd(SCPICommand.CONFIG_CURR_DC_AUTO.value)
        current = float(device.sendcmd(SCPICommand.MEASURE_CURRENT.value).replace('A', ''))
        current = float(device.sendcmd(SCPICommand.MEASURE_CURRENT.value).replace('A', ''))
    except Exception as e:
            print(f"Error during measurement: {e}")
    return voltage,current            
    
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="SCPI interface for XDM1041.")
    parser.add_argument('--port', default='COM3', help='Serial port for the XDM1041 (e.g., COM3 or /dev/ttyUSB0)')
    parser.add_argument('--baudrate', type=int, default=115200, help='Baud rate for communication (default: 115200)')
    parser.add_argument('--duration', type=int, default=7200, help='Duration of the measurement in seconds (default: 60)')
    parser.add_argument('--interval', type=float, default=10.0, help='Interval between measurements in seconds (default: 1.0)')

    args = parser.parse_args()

    try:
        # Initialize SCPI interface
        device = SCPI(port_dev=args.port, speed=args.baudrate)
        print(f"Connected to device on port {args.port}")

        # Query device identification
        idn = device.sendcmd(SCPICommand.IDENTIFY.value)
        print(f"Device ID: {idn}")

        print(device.sendcmd(SCPICommand.BEEP_STATUS.value))

        # Perform voltage and current measurements
       # measure_voltage_current(device, args.duration, args.interval)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        del device


if __name__ == "__main__":
    main()
  