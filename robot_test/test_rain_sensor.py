#!/usr/bin/env python3
"""
=====================================================
 CLEANA Solar Panel Cleaner Robot - Hardware Test
 Component: HW-028 RAIN SENSOR (2-wire plate only,
 no onboard comparator board)
=====================================================

This version of the HW-028 is just the sensing plate: two
exposed copper traces that act as a variable resistor - very
high resistance when dry, much lower resistance when wet.

Wiring (BCM pin numbering) - only 2 wires, no GND needed:
    Wire 1 -> Pi 3.3V
    Wire 2 -> Pi GPIO17

The Pi's internal pull-down resistor on GPIO17 completes the
circuit to ground. At rest (dry), the pin reads LOW. When the
plate is wet, its lowered resistance pulls the pin toward
3.3V, reading HIGH.

Note: this gives a simple wet/dry threshold, not a moisture
LEVEL. Sensitivity depends on water conductivity (tap water
works better than distilled water) and how much of the plate
is covered. If it feels unreliable (doesn't trigger, or
triggers randomly with noise), an external pull-down resistor
(e.g. 100k ohm between GPIO17 and GND) can sharpen the
threshold - let me know if you want that version instead.
"""

from gpiozero import DigitalInputDevice
from time import sleep

# ---- CONFIGURATION - EDIT IF NEEDED ----
SENSOR_PIN = 17

rain_sensor = DigitalInputDevice(SENSOR_PIN, pull_up=False)


def is_wet():
    return rain_sensor.value == 0  # flipped: 0 = wet, 1 = dry, on this board


def run_test():
    print("=== RAIN SENSOR TEST (HW-028, 2-wire plate) ===")
    print(f"Reading GPIO{SENSOR_PIN} every 0.5 seconds. Press Ctrl+C to stop.\n")
    print("Touch the plate with a wet finger or a few drops of water,")
    print("then dry it off, and watch the readings change below.\n")

    try:
        while True:
            if is_wet():
                print("WET - water detected on plate")
            else:
                print("DRY")
            sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped by user.")


if __name__ == "__main__":
    run_test()