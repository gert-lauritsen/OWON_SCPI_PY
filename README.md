# OWONSerial - SCPI Interface for OWON XDM1041

## Overview
`OWONSerial.py` is a Python library that provides a Serial SCPI (Standard Commands for Programmable Instruments) interface to communicate with the **OWON XDM1041** digital multimeter. It allows users to configure the device, send SCPI commands, and retrieve measurement data. The Instrument is not compatible with pyscpi, and therefor I use pyserial

## Features
- Supports **serial communication** via SCPI.
- Provides an **Enum-based command structure** for valid SCPI commands.
- Enables **voltage and current measurements**.
- Implements **continuous measurement mode** with configurable intervals.
- Allows easy **remote control** of the device via Python.

## Requirements
- Python 3.x
- `pyserial` library (for serial communication)

### Install Dependencies
```
pip install pyserial
```

## Usage

### 1️⃣ Initialize the SCPI Interface
```python
from OWONSerial import SCPI

device = SCPI(port_dev='COM3', speed=115200)  # Adjust port as needed
```

### 2️⃣ Query Device Identity
```python
from OWONSerial import SCPICommand

idn = device.sendcmd(SCPICommand.IDENTIFY.value)
print(f"Device ID: {idn}")
```

### 3️⃣ Measure Voltage and Current
```python
voltage = float(device.sendcmd(SCPICommand.MEASURE_VOLT.value).replace('V', ''))
current = float(device.sendcmd(SCPICommand.MEASURE_CURRENT.value).replace('A', ''))
print(f"Voltage: {voltage} V, Current: {current} A")
```

### 4️⃣ Perform Continuous Measurements
```python
from OWONSerial import measure_voltage_current

measure_voltage_current(device, duration=600, interval=5)  # Measure for 10 minutes every 5s
```

### 5️⃣ Close the Connection
```python
del device  # Ensures proper closing of the serial port
```

## Command Reference (SCPI Enum)
All valid SCPI commands are stored in `SCPICommand` Enum:

```python
from OWONSerial import SCPICommand

print(SCPICommand.MEASURE_VOLT.value)  # Outputs: "MEAS:VOLT?"
```

### SCPI Commands:
| Command | Description |
|---------|-------------|
| `SCPICommand.IDENTIFY` | Query device ID |
| `SCPICommand.MEASURE_VOLT` | Measure voltage |
| `SCPICommand.MEASURE_CURRENT` | Measure current |
| `SCPICommand.BEEP_ON` | Enable device beep |
| `SCPICommand.BEEP_OFF` | Disable device beep |
| `SCPICommand.MEASURE_1` | Measure first channel |
| `SCPICommand.MEASURE_2` | Measure second channel |
| `SCPICommand.MEASURE_SHOW` | Show measurement results |
| `SCPICommand.AUTO` | Enable auto-ranging mode |
| `SCPICommand.RANGE_SET` | Set manual range |
| `SCPICommand.RATE` | Set measurement rate |
| `SCPICommand.CONTINUITY_THRESHOLD` | Set continuity test threshold |
| `SCPICommand.CALC_FUNC` | Enable mathematical functions |
| `SCPICommand.CALC_DB_REF` | Set reference level for dB calculation |
| `SCPICommand.CALC_DBM_REF` | Set reference power for dBm calculation |
| `SCPICommand.CALC_AVERAGE_QUERY` | Query the average measurement |
| `SCPICommand.CALC_MIN_QUERY` | Query the minimum measurement |
| `SCPICommand.CALC_MAX_QUERY` | Query the maximum measurement |
| `SCPICommand.CALC_OFF` | Disable all calculations |
| `SCPICommand.RESET` | Reset the device |

## Command-Line Usage
You can also run the script directly from the terminal:
```
python OWONSerial.py --port COM3 --baudrate 115200 --duration 600 --interval 5
```
This will **measure voltage and current every 5 seconds for 10 minutes**.

## License
This project is licensed under the **MIT License**.

## Author
Created by **Gert** on January 28, 2025.

---
For more details, check the official **SCPI command reference** for the OWON XDM1041 multimeter.


