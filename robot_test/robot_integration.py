#!/usr/bin/env python3
"""
=====================================================
 CLEANA Solar Panel Cleaner Robot - Integration Test
 Wheel motors + Brush motors + Rain sensor
=====================================================

Combines the previously-tested components into one interactive
script:
  - w/s/a/d/x  -> drive the two wheel motors (BTS7960 drivers)
  - 1          -> toggle LEFT brush on/off
  - 2          -> toggle RIGHT brush on/off
  - b          -> toggle BOTH brushes together
  - q          -> quit

Rain sensor is currently disabled (see is_wet() below).

--------------------- WIRING SUMMARY ---------------------
Left brush motor (its own H-bridge, validated working config):
    IN1 -> GPIO23   IN2 -> GPIO24   ENA -> GPIO18

Right brush motor (its own H-bridge - NEW, needs wiring):
    IN1 -> GPIO22   IN2 -> GPIO27   ENA -> GPIO25

Left wheel motor (BTS7960):
    RPWM -> GPIO5   LPWM -> GPIO6   R_EN -> GPIO13   L_EN -> GPIO19

Right wheel motor (BTS7960):
    RPWM -> GPIO16  LPWM -> GPIO20  R_EN -> GPIO21   L_EN -> GPIO26

Rain sensor (2-wire plate, currently unused):
    Wire 1 -> Pi 3.3V     Wire 2 -> GPIO17
------------------------------------------------------------
"""

from gpiozero import Motor, PWMOutputDevice, DigitalOutputDevice
from time import sleep
import threading

# ---------------- CONFIGURATION ----------------
SPEED = 0.6  # wheel drive speed, 0.0 - 1.0
BRUSH_SPEED = 1.0  # brush motor speed, 0.0 - 1.0
RAIN_CHECK_INTERVAL = 0.5  # seconds between background rain checks

# ---------------- LEFT BRUSH MOTOR (validated working config) ----------------
left_brush_motor = Motor(forward=23, backward=24, enable=18)

# ---------------- RIGHT BRUSH MOTOR (its own H-bridge - new wiring) ----------------
right_brush_motor = Motor(forward=22, backward=27, enable=25)

# ---------------- LEFT WHEEL MOTOR (BTS7960) ----------------
left_rpwm = PWMOutputDevice(5)
left_lpwm = PWMOutputDevice(6)
left_r_en = DigitalOutputDevice(13)
left_l_en = DigitalOutputDevice(19)

# ---------------- RIGHT WHEEL MOTOR (BTS7960) ----------------
right_rpwm = PWMOutputDevice(16)
right_lpwm = PWMOutputDevice(20)
right_r_en = DigitalOutputDevice(21)
right_l_en = DigitalOutputDevice(26)

# ---------------- RAIN SENSOR (disabled for now) ----------------
# Rain sensor readings were unreliable, so it's disabled here.
# is_wet() always returns False until this is revisited.
def is_wet():
    return False


# ---------------- WHEEL CONTROL ----------------
def enable_wheel_drivers():
    left_r_en.on()
    left_l_en.on()
    right_r_en.on()
    right_l_en.on()


def disable_wheel_drivers():
    left_r_en.off()
    left_l_en.off()
    right_r_en.off()
    right_l_en.off()


def stop_wheels():
    left_rpwm.value = 0
    left_lpwm.value = 0
    right_rpwm.value = 0
    right_lpwm.value = 0


def forward():
    left_lpwm.value = 0
    right_lpwm.value = 0
    left_rpwm.value = SPEED
    right_rpwm.value = SPEED


def backward():
    left_rpwm.value = 0
    right_rpwm.value = 0
    left_lpwm.value = SPEED
    right_lpwm.value = SPEED


def turn_left():
    left_rpwm.value = 0
    right_lpwm.value = 0
    left_lpwm.value = SPEED
    right_rpwm.value = SPEED


def turn_right():
    left_lpwm.value = 0
    right_rpwm.value = 0
    left_rpwm.value = SPEED
    right_lpwm.value = SPEED


# ---------------- BRUSH CONTROL ----------------
left_brush_running = False
right_brush_running = False
brush_lock = threading.Lock()


def start_left_brush():
    global left_brush_running
    with brush_lock:
        left_brush_motor.forward(BRUSH_SPEED)
        left_brush_running = True
    print("Left brush ON")


def stop_left_brush(reason=""):
    global left_brush_running
    with brush_lock:
        left_brush_motor.stop()
        left_brush_running = False
    print(f"Left brush OFF{' - ' + reason if reason else ''}")


def toggle_left_brush():
    if left_brush_running:
        stop_left_brush()
    else:
        start_left_brush()


def start_right_brush():
    global right_brush_running
    with brush_lock:
        right_brush_motor.forward(BRUSH_SPEED)
        right_brush_running = True
    print("Right brush ON")


def stop_right_brush(reason=""):
    global right_brush_running
    with brush_lock:
        right_brush_motor.stop()
        right_brush_running = False
    print(f"Right brush OFF{' - ' + reason if reason else ''}")


def toggle_right_brush():
    if right_brush_running:
        stop_right_brush()
    else:
        start_right_brush()


def toggle_both_brushes():
    # If either is running, turn both off; otherwise turn both on.
    if left_brush_running or right_brush_running:
        stop_left_brush()
        stop_right_brush()
    else:
        start_left_brush()
        start_right_brush()


# ---------------- BACKGROUND RAIN MONITOR (inactive while is_wet() is disabled) ----------------
def rain_monitor():
    while not stop_event.is_set():
        if is_wet():
            if left_brush_running:
                stop_left_brush(reason="rain detected mid-clean, auto-stopped for safety")
            if right_brush_running:
                stop_right_brush(reason="rain detected mid-clean, auto-stopped for safety")
        sleep(RAIN_CHECK_INTERVAL)


stop_event = threading.Event()


def run():
    print("=== ROBOT INTEGRATION TEST ===")
    print("Controls: w=forward  s=backward  a=turn left  d=turn right  x=stop wheels")
    print("          1=toggle left brush  2=toggle right brush  b=toggle both brushes")
    print("          q=quit\n")

    enable_wheel_drivers()

    monitor_thread = threading.Thread(target=rain_monitor, daemon=True)
    monitor_thread.start()

    try:
        while True:
            cmd = input("Command> ").strip().lower()
            if cmd == "w":
                print("Moving forward...")
                forward()
            elif cmd == "s":
                print("Moving backward...")
                backward()
            elif cmd == "a":
                print("Turning left...")
                turn_left()
            elif cmd == "d":
                print("Turning right...")
                turn_right()
            elif cmd == "x":
                print("Stopping wheels.")
                stop_wheels()
            elif cmd == "1":
                toggle_left_brush()
            elif cmd == "2":
                toggle_right_brush()
            elif cmd == "b":
                toggle_both_brushes()
            elif cmd == "q":
                print("Quitting.")
                break
            else:
                print("Unknown command. Use w/s/a/d/x/1/2/b/q.")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        stop_event.set()
        stop_wheels()
        disable_wheel_drivers()
        stop_left_brush()
        stop_right_brush()
        print("All motors stopped safely. Exiting.")


if __name__ == "__main__":
    run()