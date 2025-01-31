# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 20:57:28 2025

@author: gert lauritsen
"""

import time
import OWONSerial
import argparse
import sys
import matplotlib.pyplot as plt
import keyboard
import csv
import datetime

from OWONSerial import SCPICommand
# Configuration

XDM1141_ADDRESS = "ASRL3::INSTR"  # Replace with your device's VISA address
MEASUREMENT_INTERVAL = 1  # Interval between measurements (in seconds)
TEST_DURATION = 60  # Total test duration (in seconds)
CHECK_INTERVAL = 0.1       # Check for keypress every 0.1s

def plot_voltage_curve(timestamps, voltages):
    """Plots the voltage curve over time."""
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, voltages, label="Voltage", color="blue", linewidth=2)


    # Add labels, title, and legend
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("Voltage vs Time")
    plt.legend()
    plt.grid()
    plt.show()

def SaveToCSV (timestamps, voltages):
    # Generate filename based on current date & time
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{current_time}_voltage.dat"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
    
        # Write header
        writer.writerow(["Timestamp", "Voltage"])
    
        # Write data
        for ts, v in zip(timestamps, voltages):
            writer.writerow([ts, v])

    print("CSV file saved as 'data.csv'")    

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="SCPI interface for XDM1041.")
    parser.add_argument('--port', default='COM3', help='Serial port for the XDM1041 (e.g., COM3 or /dev/ttyUSB0)')
    parser.add_argument('--baudrate', type=int, default=115200, help='Baud rate for communication (default: 115200)')
    parser.add_argument('--duration', type=int, default=7200, help='Duration of the measurement in seconds (default: 60)')
    parser.add_argument('--interval', type=float, default=1.0, help='Interval between measurements in seconds (default: 1.0)')
    
    print(sys.modules.get("OWONSerial"))
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
        device.sendcmd(SCPICommand.CONF_VOLT_DC_AUTO.value)        
        print(f"Device ID: {idn}")
        print("Press q to stop measurement")
        measurement=True
        while measurement:
            # Perform voltage and current measurements
            V= float(device.sendcmd(SCPICommand.MEASURE_VOLT.value).replace('V', ''))
            # Store data

            voltages.append(V)
            elapsed_time = time.time() - start_time
            timestamps.append(elapsed_time)
            print(f"Time: {elapsed_time:.2f}s, {V:.5f} V")

            # Wait for the next measurement interval
            elapsed_time = 0
            while elapsed_time < MEASUREMENT_INTERVAL:
                if keyboard.is_pressed('q'):  # Check if 'q' is pressed
                    print("Measurement stopped!")
                    measurement=False  # Exit program immediately (or use `break` if inside another loop)
        
                time.sleep(CHECK_INTERVAL)
                elapsed_time += CHECK_INTERVAL
    except Exception as e:
        print(f"Error: {e}")
    finally:
        del device
        plot_voltage_curve(timestamps,voltages)
        print("Measurement completed.")
        # Plot the results
        key = input("Press Enter to continue...")

if __name__ == "__main__":
    main()
