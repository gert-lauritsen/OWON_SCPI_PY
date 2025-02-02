# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 20:46:20 2025

@author: gert
"""

# -*- coding: utf-8 -*-
"""
Updated to use PyVISA instead of pyserial
"""

import pyvisa
import argparse
import time
from enum import Enum


class SCPICommand(Enum):
    # System Commands
    IDENTIFY = "*IDN?"                  # Query device identification (manufacturer, model, serial number, firmware version)
    REMOTE_MODE = "SYST:REM"            # Set device to remote control mode
    LOCAL_MODE = "SYST:LOC"             # Return device to local (manual) control mode

    # Measurement Commands
    MEASURE = "MEAS?"                   # Query the latest measurement (depends on the current function mode)
    MEASURE_VOLT = "MEAS:VOLT?"         # Query the measured voltage
    MEASURE_CURRENT = "MEAS:CURRENT?"   # Query the measured current

    # Function Selection
    FUNCTION = "FUNC?"                  # Query the current function mode (Voltage, Current, Resistance, etc.)

    # Configuration Commands
    CONF_VOLT_DC_AUTO = "CONF:VOLT:DC AUTO"  # Configure voltage measurement in DC auto-ranging mode
    CONF_VOLT_DC = "CONF:VOLT:DC"       # Configure voltage measurement in DC mode (manual range)
    CONF_CURR_DC_AUTO = "CONF:CURR:DC AUTO"  # Configure current measurement in DC auto-ranging mode
    CONF_CURR_DC = "CONF:CURR:DC"       # Configure current measurement in DC mode (manual range)
    CONF_RES_AUTO = "CONF:RES AUTO"     # Configure resistance measurement in auto-ranging mode

    # Beep Control
    BEEP_ON = "BEEP:STAT ON"            # Enable device beep sound
    BEEP_OFF = "BEEP:STAT OFF"          # Disable device beep sound

    # Reset
    RESET = "*RST"                      # Reset the device to factory default settings



def measure_voltage_current(device, duration, interval):
    """
    Measure voltage and current for the specified duration and interval.
    """
    print("Starting measurements...")
    print("Time (s), Voltage (V), Current (A)")

    elapsed_time = 0
    start_time = time.time()
    cycle_time=interval/2
    while elapsed_time < duration:
        try:
            cycle_start = time.time()

            # Measure voltage
            device.write (SCPICommand.CONF_VOLT_DC_AUTO.value)
            time.sleep(cycle_time/2)
            voltage = float(device.query(SCPICommand.MEASURE_VOLT.value).replace('V', ''))

            # Measure current
            device.write(SCPICommand.CONF_CURR_DC_AUTO.value)
            time.sleep(cycle_time/2)
            current = float(device.query(SCPICommand.MEASURE_CURRENT.value).replace('A', ''))
            elapsed_time = time.time()-start_time
            print(f"{elapsed_time:6.1f}, {voltage:9.5f}, {current:9.5f}")

        except Exception as e:
            print(f"Error during measurement: {e}")

        # Adjust sleep time
        cycle_time = time.time() - cycle_start

    print("Measurements completed.")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="SCPI interface for instruments using PyVISA.")
    parser.add_argument('--resource', default='ASRL3::INSTR', help='VISA resource string (e.g., USB0::0x1AB1::0x0588::INSTR)')
    parser.add_argument('--duration', type=int, default=100, help='Duration of the measurement in seconds (default: 10)')
    parser.add_argument('--interval', type=float, default=10.0, help='Interval between measurements in seconds (default: 1.0)')

    args = parser.parse_args()

    try:
        # Initialize SCPI interface
        rm = pyvisa.ResourceManager()
        print(rm.list_resources())
        OWON=rm.open_resource(resource_name=args.resource)
        OWON.baud_rate=115200 # this is how to make it run with visa !!!!
        print(OWON.query("*IDN?"))        
        # Perform voltage and current measurements
        measure_voltage_current(OWON, args.duration, args.interval)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        OWON.close()


if __name__ == "__main__":
    main()
