import time

from config import *

def com():
    response = "+04.363+04.366+04.432+05.000+04.000+12.360+15.100+00.000"

    # ser1 = serial.Serial(port=comport, baudrate=9600, timeout=2)
    # if not ser1.is_open:
    #     ser1.open()
    # # print('serial Port1 Open for sending #01')
    #
    # ser1.flush()
    # ser1.flushInput()
    # ser1.flushOutput()
    # ser1.write(b'#01\r')
    # time.sleep(0.03)
    # response = ser1.readline().decode('ascii')
    # ser1.flush()
    # ser1.flushInput()
    # ser1.flushOutput()
    # ser1.close()
    received_buffer = response
    with open('raw_data.txt','w+') as file:
        file.write(received_buffer)
        file.close()

    # calculating RAIN FALL
    raw_data_list = list(received_buffer.split('+'))
    tbrg = raw_data_list[4]
    print(tbrg)
    rainfall = float(tbrg) * resolution_val
    print(rainfall)
    return rainfall

def rain_count():
    try:
        with open('current_rainfall.txt', 'r') as file1:
            pre_rain_fall = file1.read().strip()

        current_rainfall = float(pre_rain_fall) + com()
        print(current_rainfall)

        with open('current_rainfall.txt', 'w+') as file2:
            file2.write(str(current_rainfall))

    except FileNotFoundError:
        print("Error: 'current_rainfall.txt' not found.")
    except ValueError:
        print("Error: Unable to convert the current rainfall to a float. Check for non-numeric characters.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__  == "__main__":
    while True:
        rain_count()
        time.sleep(10) # update after 5 minute interval
