import serial
import pyautogui

ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust the serial port as necessary
last_key = None

while True:
    try:
        if ser.inWaiting() > 0:
            key = ser.read().decode().strip()

            if key == 'N':  # Reset last_key when no key is pressed
                last_key = None
                continue

            if key and key != last_key:
                last_key = key

                # Map Arduino key codes to corresponding actions
                if key == "A":
                    pyautogui.press('+')
                elif key == "B":
                    pyautogui.press('-')
                elif key == "C":
                    pyautogui.press('.')
                elif key == "D":
                    pyautogui.press('/')
                elif key == "#":
                    pyautogui.press('enter')
                elif key == "*":
                    pyautogui.press('backspace')
                elif key.isdigit():
                    pyautogui.write(key)  # Typing numbers

    except KeyboardInterrupt:
        break

ser.close()
