#!/usr/bin/env python3
"""
=====================================================
 CLEANA Solar Panel Cleaner Robot - Hardware Test
 Component: RIGHT MOVEMENT MOTOR (power window motor)
=====================================================

Wiring (2nd L298N driver, Channel B, BCM pin numbering):
    L298N ENB  -> Raspberry Pi GPIO12 (PWM)
    L298N IN3  -> Raspberry Pi GPIO16
    L298N IN4  -> Raspberry Pi GPIO20
    L298N OUT3/OUT4 -> Right wheel motor terminals
    L298N +12V -> External battery positive
    L298N GND  -> Battery negative AND Raspberry Pi GND (common ground!)

Edit the three pin numbers below if your wiring is different.
"""

from gpiozero import Motor
from time import sleep

# ---- GPIO PIN CONFIGURATION (BCM numbering) - EDIT THESE IF NEEDED ----
IN3 = 16   # L298N IN3
IN4 = 20   # L298N IN4
ENB = 12   # L298N ENB (PWM / speed control)

right_motor = Motor(forward=IN3, backward=IN4, enable=ENB)


def run_test():
    print("=== RIGHT MOTOR TEST ===")
    print("Lift the robot so the wheels can spin freely, or clear the drive path.")
    input("Press Enter when ready to start...")

    print("\n[1/3] Wheel FORWARD at 50% speed for 3 seconds")
    right_motor.forward(0.5)
    sleep(3)
    right_motor.stop()
    sleep(1)

    print("[2/3] Wheel FORWARD at 100% speed for 3 seconds")
    right_motor.forward(1.0)
    sleep(3)
    right_motor.stop()
    sleep(1)

    print("[3/3] Wheel BACKWARD at 50% speed for 3 seconds")
    right_motor.backward(0.5)
    sleep(3)
    right_motor.stop()

    print("\nTest complete - right motor stopped.")


if __name__ == "__main__":
    try:
        run_test()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        right_motor.stop()
        print("Motor safely stopped. Exiting.")
