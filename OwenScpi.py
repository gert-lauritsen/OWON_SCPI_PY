# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 16:35:14 2025

@author: gert
"""

import pyvisa
from enum import Enum

class VoltageRange(Enum):
    """Valid voltage ranges for DC and AC modes"""
    MIN = "50E-3"   # 50mV
    LOW = "500E-3"  # 500mV
    MID = "5"       # 5V
    HIGH = "50"     # 50V
    MAX = "1000"    # 1000V

class CurrentRange(Enum):
    """Valid current ranges for DC and AC modes"""
    MIN = "500E-6"  # 500µA
    LOW = "5E-3"    # 5mA
    MID = "500E-3"  # 500mA
    HIGH = "5"      # 5A
    MAX = "10"      # 10A

class TemperatureUnit(Enum):
    """Temperature units"""
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"

class MeasurementSpeed(Enum):
    """Measurement speed settings"""
    SLOW = "S"
    MEDIUM = "M"
    FAST = "F"

class SCPIInstrument:
    """
    Class for communicating with SCPI instruments using PyVISA.
    """

    def __init__(self, resource_name):
        """Initialize connection to the instrument."""
        rm = pyvisa.ResourceManager()
        self.device = rm.open_resource(resource_name)
        self.device.baud_rate=115200
        self.device.write_termination = '\n'
        self.device.read_termination = '\n'

    def send_command(self, command):
        """Send a command without expecting a response."""
        self.device.write(command)

    def query(self, command):
        """Send a command and return the response."""
        return self.device.query(command).strip()

    # 🔹 System Commands
    def get_identity(self):
        """Query device identification."""
        return self.query("*IDN?")

    def set_remote_mode(self):
        """Switch to remote mode (lock front panel buttons)."""
        self.send_command("SYST:REM")

    def set_local_mode(self):
        """Switch to local mode (unlock front panel buttons)."""
        self.send_command("SYST:LOC")

    # 🔹 Measurement Commands
    def measure_voltage(self):
        """Query the measured voltage."""
        return float(self.query("MEAS:VOLT?"))

    def measure_current(self):
        """Query the measured current."""
        return float(self.query("MEAS:CURRENT?"))

    def measure_all(self):
        """Query all active measurements."""
        return self.query("MEAS?")

    # Function Selection
    def function(self):
        #Returns the current function on the main display. One of the following:
        return self.query("FUNC?")
    
    def funktion1(self):
        #Returns the current function on the main display. One of the following:
        return self.query("FUNC1?")

    def funktion2(self):
        #Returns the current function on the secondary display. One of the following:
        return self.query("FUNC2?")

    # 🔹 Voltage Configuration
    def configure_voltage_dc(self, range_value: VoltageRange):
        """Configure DC voltage measurement with specified range."""
        self.send_command(f"CONF:VOLT:DC {range_value.value}")

    def configure_voltage_ac(self, range_value: VoltageRange):
        """Configure AC voltage measurement with specified range."""
        self.send_command(f"CONF:VOLT:AC {range_value.value}")

    # 🔹 Current Configuration
    def configure_current_dc(self, range_value: CurrentRange):
        """Configure DC current measurement with specified range."""
        self.send_command(f"CONF:CURR:DC {range_value.value}")

    def configure_current_ac(self, range_value: CurrentRange):
        """Configure AC current measurement with specified range."""
        self.send_command(f"CONF:CURR:AC {range_value.value}")

    # 🔹 Temperature Configuration
    def set_temperature_unit(self, unit: TemperatureUnit):
        """Set the temperature unit (Celsius, Fahrenheit, Kelvin)."""
        self.send_command(f"TEMP:RTD:UNIT {unit.value}")

    def get_temperature_unit(self):
        """Query the current temperature unit."""
        return self.query("TEMP:RTD:UNIT?")

    # 🔹 Measurement Speed
    def set_measurement_speed(self, speed: MeasurementSpeed):
        """Set measurement speed (slow, medium, fast)."""
        self.send_command(f"RATE {speed.value}")

    def get_measurement_speed(self):
        """Query measurement speed setting."""
        return self.query("RATE?")

    # 🔹 Beep Control   #Beep command isn't supported
    def beep_on(self):
        """Enable device beep sound."""
        self.send_command("BEEP:STAT ON") #dos not gives any respons return

    def beep_off(self):
        """Disable device beep sound."""
        self.send_command("BEEP:STAT OFF")

    def query_beep_status(self):
        """Query if beep is ON or OFF.""" # GIves an error, like the command is not supported
        return self.query("BEEP:STAT?")

    # 🔹 Reset
    def reset_device(self):
        """Reset the device to factory default settings."""
        self.send_command("*RST")

    def close(self):
        """Close the connection to the instrument."""
        self.device.close()


def main():
    # Initialize instrument
    device = SCPIInstrument("ASRL3::INSTR")

    # Query device identity
    print(device.get_identity())

    # Configure measurement settings
    device.configure_voltage_dc(VoltageRange.MID)  # Set to 5V range
    device.configure_current_dc(CurrentRange.MIN)  # Set to 500µA range
    device.set_measurement_speed(MeasurementSpeed.FAST)

    # Perform measurements
    voltage = device.measure_voltage()
    current = device.measure_current()
    print(f"Voltage: {voltage} V, Current: {current} A")
    
    # Control beep sound
  #  print(device.function())
  #  print(device.get_measurement_speed())
  #  device.beep_on()
  #   status = device.query_beep_status()
  #  print(f"Beep status: {status}")
    print("Close Instrument")
    # Cleanup
    device.close()

if __name__ == "__main__":
    main()
