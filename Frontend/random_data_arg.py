import random
import time
import datetime
import mysql.connector

mydb = mysql.connector.connect(user='root', password='admin', host='localhost', database='wrd_dash', auth_plugin='mysql_native_password')

stn_type = ['ARG']
stn_location = ['Harbhangi', 'Saipala','Badanalla']
stn_id = ['11001002', '12301001', '12401003']
stn_nm = ['ARG_002', 'ARG_001', 'ARG_003']
def data_generation():
    for location, station_id, stn_name in zip(stn_location, stn_id, stn_nm):
        # Access the current elements from each list
        # print("Location:", location)
        # print("Station ID:", station_id)
        # print("Station Name:", stn_name)

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M')
        hourly_rainfall = round(random.uniform(0, 30), 3)
        daily_rainfall_value = round(random.uniform(0, 30), 3)
        rainfall_value_8am = round(random.uniform(0, 30), 3)
        battery_voltage = round(random.uniform(0, 30), 3)
        solar_voltage = round(random.uniform(0, 30), 3)
        mycursor = mydb.cursor()
        sql = "INSERT INTO arg(stn_id, stn_type, stn_nm, location, hourly_rainfall,daily_rainfall,rainfall_value_8am, battery_voltage, solar_voltage, datetime) VALUES (%s, %s, %s, %s,%s, %s,%s, %s, %s, %s)"
        try:
            mycursor.execute(sql, (
            station_id, stn_type[0], stn_name, location, hourly_rainfall,daily_rainfall_value, rainfall_value_8am,battery_voltage, solar_voltage, timestamp))
            mydb.commit()
            print(mycursor.rowcount, "row inserted into the database")
        except Exception as e:
            print("Something went wrong:", e)
            mydb.rollback()

while True:
 data_generation()
 time.sleep(60)