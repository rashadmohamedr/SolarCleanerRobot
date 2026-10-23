#!/usr/bin/env python3
"""
=====================================================
 CLEANA Solar Panel Cleaner Robot - Hardware Test
 Component: BRUSH MOTOR (cleaning brush DC gear motor)
=====================================================

Wiring (L298N driver, BCM pin numbering):
    L298N ENA  -> Raspberry Pi GPIO18 (must stay a PWM pin)
    L298N IN1  -> Raspberry Pi GPIO23
    L298N IN2  -> Raspberry Pi GPIO24
    L298N OUT1/OUT2 -> Brush motor terminals
    L298N +12V -> External battery positive
    L298N GND  -> Battery negative AND Raspberry Pi GND (common ground!)

If your wiring differs, just change the three pin numbers below.
"""

from gpiozero import Motor
from time import sleep

# ---- GPIO PIN CONFIGURATION (BCM numbering) - EDIT THESE IF NEEDED ----
IN1 = 23   # L298N IN1
IN2 = 24   # L298N IN2
ENA = 18   # L298N ENA (PWM / speed control)

brush_motor = Motor(forward=IN1, backward=IN2, enable=ENA)


def run_test():
    print("=== BRUSH MOTOR TEST ===")
    print("Make sure the brush is clear of fingers, cables, and the panel surface.")
    input("Press Enter when ready to start...")

    print("\n[1/3] Spinning FORWARD at 50% speed for 3 seconds")
    brush_motor.forward(0.5)
    sleep(3)
    brush_motor.stop()
    sleep(1)

    print("[2/3] Spinning FORWARD at 100% speed for 3 seconds")
    brush_motor.forward(1.0)
    sleep(3)
    brush_motor.stop()
    sleep(1)

    print("[3/3] Spinning BACKWARD (reverse) at 50% speed for 3 seconds")
    brush_motor.backward(0.5)
    sleep(3)
    brush_motor.stop()

    print("\nTest complete - brush motor stopped.")


if __name__ == "__main__":
    try:
        run_test()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        brush_motor.stop()
        print("Motor safely stopped. Exiting.")
