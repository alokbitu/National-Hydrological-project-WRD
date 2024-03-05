import random
import time
import datetime
import mysql.connector

mydb = mysql.connector.connect(user='root', password='admin', host='localhost', database='wrd', auth_plugin='mysql_native_password')

stn_type = ['ARS','AWLR','AWLR_ARS']
stn_location = ['Bridge1','Bridge2','Bridge3','Bridge4','Bridge5','Bridge6']
# stn_id = ['1RUKHSA005','3RUKHSA001','2RUCTAB001','2RUCTAA002','1RUKHSA004','3RUKHSA004']
stn_id_ARS = ['2RUCTAB001','2RUCTAB002','2RUCTAB003']
stn_id_AWLR = ['1BRRSRE001','1BRRSMA002','1BRRSPI003']
stn_id_Combine = ['3RUKHSA001','3RUKHSA002','3RUKHSA003']
def calculation():
    # rainfall = random.uniform(0,30)
    # print(round(rainfall),3)
    # water_level_value = random.uniform(0,30)
    # print(round(water_level_value),3)
    # battery_voltage = random.uniform(0,30)
    # print(round(battery_voltage),3)
    # solar_voltage = random.uniform(0,30)
    # print(round(solar_voltage),3)
    # # time.sleep(5)
    # return rainfall,water_level_value,battery_voltage,solar_voltage
    rainfall = round(random.uniform(0, 30), 3)
    water_level_value = round(random.uniform(0, 30), 3)
    battery_voltage = round(random.uniform(0, 30), 3)
    solar_voltage = round(random.uniform(0, 30), 3)
    return rainfall, water_level_value, battery_voltage, solar_voltage


def stn_details():

    station_type = random.choice(stn_type)
    # print(station_type)
    station_location = random.choice(stn_location)
    # print(station_location)
    # station_id = random.choice(stn_id)
    if station_type == 'ARS':
        station_id = random.choice(stn_id_ARS)
    if station_type == 'AWLR':
        station_id = random.choice(stn_id_AWLR)
    if station_type == 'AWLR_ARS':
        station_id = random.choice(stn_id_Combine)
    print(station_id)
    return station_id,station_location,station_type


def db_insert():


    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M')
    mycursor = mydb.cursor()
    sql = "INSERT INTO realtime_data_query_table(stn_id, stn_location, datetime, stn_type, rainfall_value, water_level_value, battery_voltage, solar_voltage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    try:
     rainfall, water_level_value, battery_voltage, solar_voltage = calculation()
     station_id, station_location, station_type = stn_details()
     mycursor.execute(sql, (station_id, station_location, timestamp, station_type, rainfall, water_level_value, battery_voltage, solar_voltage))
     mydb.commit()
     print(mycursor.rowcount, "details inserted")

    except Exception as e:
     print("Something went wrong:", e)
     mycursor.close()
     mydb.close()


if __name__  == '__main__':
    while True:
        db_insert()
        time.sleep(60)

