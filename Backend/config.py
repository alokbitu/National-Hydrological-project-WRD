MinMa = 4
MaxMa = 20
maxAbs = 20
multiplyFactors =1
location = 'ODSW'
station_id = '&31801040'
station_number = '31801040'
sim_number = 8093027310
comport = '/dev/ttyAMA4'
hourly_rainfall_list = []
daily_rainfall_list = []

with open('rl_value.txt', 'r') as file:
    rl_value = float(file.read())
    file.close()
with open('water_height.txt', 'r') as file:
    water_height = float(file.read())
    file.close()
with open('resolution_value.txt','r') as file2:
    resolution_val = float(file2.read())
    file2.close()