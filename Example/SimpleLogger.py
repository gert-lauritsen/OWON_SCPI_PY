# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 20:57:28 2025

@author: gert
"""

#import pyvisa
import time
import OWONSerial
import argparse


# Configuration

XDM1141_ADDRESS = "ASRL3::INSTR"  # Replace with your device's VISA address
MEASUREMENT_INTERVAL = 1  # Interval between measurements (in seconds)
TEST_DURATION = 60  # Total test duration (in seconds)


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="SCPI interface for XDM1041.")
    parser.add_argument('--port', default='COM3', help='Serial port for the XDM1041 (e.g., COM3 or /dev/ttyUSB0)')
    parser.add_argument('--baudrate', type=int, default=115200, help='Baud rate for communication (default: 115200)')
    parser.add_argument('--duration', type=int, default=7200, help='Duration of the measurement in seconds (default: 60)')
    parser.add_argument('--interval', type=float, default=1.0, help='Interval between measurements in seconds (default: 1.0)')

    # Prepare data storage
    timestamps = []
    voltages = []
    
    args = parser.parse_args()
    start_time = time.time()  # Record the start time
    try:
        # Initialize SCPI interface
        device = OWONSerial.SCPI(port_dev=args.port, speed=args.baudrate)
        print(f"Connected to device on port {args.port}")

        # Query device identification
        idn = device.sendcmd(SCPICommand.IDENTIFY.value)
        print(f"Device ID: {idn}")
        while True:
            # Perform voltage and current measurements
            V=device.sendcmd(SCPICommand.MEASURE_VOLT.value)
            # Store data

            voltages.append(V)
            elapsed_time = time.time() - start_time
            timestamps.append(elapsed_time)
            print(f"Time: {elapsed_time:.2f}s, Voltage: {V:.5f} V")

            # Wait for the next measurement interval
            time.sleep(MEASUREMENT_INTERVAL)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        del device    
        print("Measurement completed.")
        # Plot the results
