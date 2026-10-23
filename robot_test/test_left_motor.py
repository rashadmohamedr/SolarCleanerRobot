#!/usr/bin/env python3
"""
=====================================================
 CLEANA Solar Panel Cleaner Robot - Hardware Test
 Component: LEFT MOVEMENT MOTOR (power window motor)
=====================================================

Wiring (2nd L298N driver, BCM pin numbering):
    L298N ENA  -> Raspberry Pi GPIO13 (PWM)
    L298N IN1  -> Raspberry Pi GPIO5
    L298N IN2  -> Raspberry Pi GPIO6
    L298N OUT1/OUT2 -> Left wheel motor terminals
    L298N +12V -> External battery positive
    L298N GND  -> Battery negative AND Raspberry Pi GND (common ground!)

Edit the three pin numbers below if your wiring is different.
"""

from gpiozero import Motor
from time import sleep

# ---- GPIO PIN CONFIGURATION (BCM numbering) - EDIT THESE IF NEEDED ----
IN1 = 5    # L298N IN1
IN2 = 6    # L298N IN2
ENA = 13   # L298N ENA (PWM / speed control)

left_motor = Motor(forward=IN1, backward=IN2, enable=ENA)


def run_test():
    print("=== LEFT MOTOR TEST ===")
    print("Lift the robot so the wheels can spin freely, or clear the drive path.")
    input("Press Enter when ready to start...")

    print("\n[1/3] Wheel FORWARD at 50% speed for 3 seconds")
    left_motor.forward(0.5)
    sleep(3)
    left_motor.stop()
    sleep(1)

    print("[2/3] Wheel FORWARD at 100% speed for 3 seconds")
    left_motor.forward(1.0)
    sleep(3)
    left_motor.stop()
    sleep(1)

    print("[3/3] Wheel BACKWARD at 50% speed for 3 seconds")
    left_motor.backward(0.5)
    sleep(3)
    left_motor.stop()

    print("\nTest complete - left motor stopped.")


if __name__ == "__main__":
    try:
        run_test()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        left_motor.stop()
        print("Motor safely stopped. Exiting.")
