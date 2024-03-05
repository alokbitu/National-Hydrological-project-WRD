import random
import time
import datetime
import mysql.connector

mydb = mysql.connector.connect(user='root', password='admin', host='localhost', database='wrd_dash', auth_plugin='mysql_native_password')

stn_type = ['ARG+AWL']
stn_location = ['Sapua Badjore Dam', 'Remal Dam','Salia Dam ', 'Baghua Dam']
stn_id = ['30901017', '31701005', '31801040', '32201035']
stn_nm = ['ARG+AWL_017', 'ARG+AWL_005', 'ARG+AWL_040', 'ARG+AWL_035']
def data_generation():
    for location, station_id, stn_name in zip(stn_location, stn_id, stn_nm):
        # Access the current elements from each list
        # print("Location:", location)
        # print("Station ID:", station_id)
        # print("Station Name:", stn_name)

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M')
        daily_rainfall_value = round(random.uniform(0, 30), 3)
        rainfall_value_8am = round(random.uniform(0, 30), 3)
        water_level_value = round(random.uniform(0, 30), 3)
        water_level_value_8am = round(random.uniform(0, 30), 3)
        battery_voltage = round(random.uniform(0, 30), 3)
        solar_voltage = round(random.uniform(0, 30), 3)
        mycursor = mydb.cursor()
        sql = "INSERT INTO combine_station(stn_id, stn_type, stn_nm, location,daily_rainfall_value,rainfall_value_8am, water_level_value,water_level_8am, battery_voltage, solar_voltage, datetime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            mycursor.execute(sql, (
            station_id, stn_type[0], stn_name, location, daily_rainfall_value,rainfall_value_8am,water_level_value,water_level_value_8am, battery_voltage, solar_voltage, timestamp))
            mydb.commit()
            print(mycursor.rowcount, "row inserted into the database")
        except Exception as e:
            print("Something went wrong:", e)
            mydb.rollback()

while True:
 data_generation()
 time.sleep(60)