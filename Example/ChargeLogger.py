# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 08:45:12 2025

@author: gert
"""

#import pyvisa
import time
import matplotlib.pyplot as plt
import OWONSerial
import argparse
import keyboard

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
    parser.add_argument('--interval', type=float, default=60.0, help='Interval between measurements in seconds (default: 1.0)')

    # Prepare data storage
    timestamps = []
    voltages = []
    currents = []
    
    args = parser.parse_args()
    start_time = time.time()  # Record the start time
    try:
        # Initialize SCPI interface
        device = OWONSerial.SCPI(port_dev=args.port, speed=args.baudrate)
        print(f"Connected to device on port {args.port}")

        # Query device identification
        idn = device.sendcmd("*IDN?")
        print(f"Device ID: {idn}")
        while True:
            # Perform voltage and current measurements
            V,I=OWONSerial.measure_a_voltage_and_current(device)
            # Store data

            voltages.append(V)
            currents.append(I)
            elapsed_time = time.time() - start_time
            timestamps.append(elapsed_time)
            print(f"Time: {elapsed_time:.2f}s, Voltage: {V:.5f} V, Current: {I:.5f} A")

            # Wait for the next measurement interval
            time.sleep(MEASUREMENT_INTERVAL)
            if keyboard.is_pressed("q"):  # Change "q" to any key you want
                print("\nKey pressed! Exiting loop.")
                break            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        del device    
        print("Measurement completed.")
        # Plot the results
        plot_measurements(timestamps, voltages, currents)

def plot_measurements(timestamps, voltages, currents):
    """Plot the voltage and current over time."""
    plt.figure(figsize=(12, 6))

    # Plot voltage
    plt.subplot(2, 1, 1)
    plt.plot(timestamps, voltages, label="Voltage (V)", color="blue")
    plt.ylabel("Voltage (V)")
    plt.grid(True)
    plt.legend()

    # Plot current
    plt.subplot(2, 1, 2)
    plt.plot(timestamps, currents, label="Current (A)", color="green")
    plt.xlabel("Time (s)")
    plt.ylabel("Current (A)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()
    
    
if __name__ == "__main__":
    main()
