#!/usr/bin/env python3
"""
=====================================================
 CLEANA Solar Panel Cleaner Robot - Hardware Test
 GENERIC H-BRIDGE TEST (BTS7960 / IBT_2 driver)
 Uses RPi.GPIO directly (simpler, fewer dependencies
 than gpiozero - use this if the previous script
 failed to run or didn't move the motor).
=====================================================

Wiring (BCM pin numbering) - EDIT THESE 4 NUMBERS FOR
WHICHEVER MOTOR/BOARD YOU ARE TESTING:
    R_EN  -> Pi GPIO13
    L_EN  -> Pi GPIO19
    RPWM  -> Pi GPIO5
    LPWM  -> Pi GPIO6
    VCC   -> Pi 5V
    GND   -> Pi GND (common with battery GND)
    B+/B- -> battery
    M+/M- -> motor

RPWM = forward PWM signal, LPWM = reverse PWM signal.
R_EN and L_EN must both be HIGH for the driver to output
anything at all - this is the #1 reason a BTS7960 "does
nothing": forgetting to enable it.
"""

import RPi.GPIO as GPIO
from time import sleep

# ---- GPIO PIN CONFIGURATION (BCM numbering) - EDIT THESE ----
R_EN_PIN = 13
L_EN_PIN = 19
RPWM_PIN = 5
LPWM_PIN = 6

PWM_FREQ = 1000  # Hz

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(R_EN_PIN, GPIO.OUT)
GPIO.setup(L_EN_PIN, GPIO.OUT)
GPIO.setup(RPWM_PIN, GPIO.OUT)
GPIO.setup(LPWM_PIN, GPIO.OUT)

rpwm = GPIO.PWM(RPWM_PIN, PWM_FREQ)
lpwm = GPIO.PWM(LPWM_PIN, PWM_FREQ)
rpwm.start(0)
lpwm.start(0)


def enable_driver():
    GPIO.output(R_EN_PIN, GPIO.HIGH)
    GPIO.output(L_EN_PIN, GPIO.HIGH)
    print("Driver enabled (R_EN and L_EN set HIGH).")


def disable_driver():
    GPIO.output(R_EN_PIN, GPIO.LOW)
    GPIO.output(L_EN_PIN, GPIO.LOW)
    print("Driver disabled (R_EN and L_EN set LOW).")


def forward(duty_percent):
    lpwm.ChangeDutyCycle(0)
    rpwm.ChangeDutyCycle(duty_percent)


def backward(duty_percent):
    rpwm.ChangeDutyCycle(0)
    lpwm.ChangeDutyCycle(duty_percent)


def stop():
    rpwm.ChangeDutyCycle(0)
    lpwm.ChangeDutyCycle(0)


def run_test():
    print("=== GENERIC H-BRIDGE TEST ===")
    print(f"Pins in use -> R_EN:{R_EN_PIN}  L_EN:{L_EN_PIN}  RPWM:{RPWM_PIN}  LPWM:{LPWM_PIN}")
    print("Make sure the motor/brush is clear to move freely.")
    input("Press Enter when ready to start...")

    enable_driver()

    print("\n[1/3] FORWARD at 50% duty for 3 seconds")
    forward(50)
    sleep(3)
    stop()
    sleep(1)

    print("[2/3] FORWARD at 100% duty for 3 seconds")
    forward(100)
    sleep(3)
    stop()
    sleep(1)

    print("[3/3] BACKWARD at 50% duty for 3 seconds")
    backward(50)
    sleep(3)
    stop()

    print("\nTest complete.")


if __name__ == "__main__":
    try:
        run_test()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"\nERROR: {e}")
    finally:
        stop()
        disable_driver()
        rpwm.stop()
        lpwm.stop()
        GPIO.cleanup()
        print("GPIO cleaned up. Exiting.")