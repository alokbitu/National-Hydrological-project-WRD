import random
import time
import datetime
import mysql.connector

mydb = mysql.connector.connect(user='root', password='admin', host='localhost', database='wrd_dash', auth_plugin='mysql_native_password')

stn_type = ['AWL']
stn_location = ['Singarimunda Rd Bridge,SH-62,Singarimunda', 'Deulabeda Rd Brodge,SH-62,Deulabeda',
                    'Barsar Rd Bridge,Barsar', 'Khaeramal Rd Bridge,NH-57,Khaeramal',
                    'Jamatangi Rd Bridge,NH-57,Maheswar Pinda']
stn_id = ['20101051', '20102052', '20401018', '20601045', '20602046']
stn_nm = ['AWL_051', 'AWL_052', 'AWL_018', 'AWL_045', 'AWL_046']
def data_generation():
    for location, station_id, stn_name in zip(stn_location, stn_id, stn_nm):
        # Access the current elements from each list
        # print("Location:", location)
        # print("Station ID:", station_id)
        # print("Station Name:", stn_name)

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M')
        water_level_value = round(random.uniform(0, 30), 3)
        water_level_8am = round(random.uniform(0, 30), 3)
        battery_voltage = round(random.uniform(0, 30), 3)
        solar_voltage = round(random.uniform(0, 30), 3)
        mycursor = mydb.cursor()
        sql = "INSERT INTO awlr(stn_id, stn_type, stn_nm, location, water_level_value,water_level_8am, battery_voltage, solar_voltage, datetime) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
        try:
            mycursor.execute(sql, (
            station_id, stn_type[0], stn_name, location, water_level_value,water_level_8am, battery_voltage, solar_voltage, timestamp))
            mydb.commit()
            print(mycursor.rowcount, "row inserted into the database")
        except Exception as e:
            print("Something went wrong:", e)
            mydb.rollback()

while True:
 data_generation()
 time.sleep(60)