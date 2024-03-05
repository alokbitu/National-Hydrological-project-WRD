import csv
import os
import time
from datetime import datetime
import shutil

import mysql.connector

mydb = mysql.connector.connect(user='root', password='admin', host='localhost', database='wrd_dash', auth_plugin='mysql_native_password')

def data_reading():
    # Source folder path containing CSV files
    source_folder_path = 'D:\\ARPITA\\COMPLETED Projects\\WRD_Dash_final\\WRD_final\\wrd_csv_files'

    # Destination folder path to move processed CSV files
    destination_folder_path = 'D:\\ARPITA\\COMPLETED Projects\\WRD_Dash_final\\WRD_final\\processed_csv_files'

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)

    while True:
        # Get all files in the source folder
        files = os.listdir(source_folder_path)
        # Filter out only the CSV files
        csv_files = [file for file in files if file.endswith('.csv')]

        for csv_file in csv_files:
            file_path = os.path.join(source_folder_path, csv_file)
            # print(file_path)
            # time.sleep(1)
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                for data in csv_reader:
                    #print(data)
                    if len([column.strip() for column in data]) == 9 :  # Check if the row has 7 columns
                        stn_id = data[0]
                        list_of_characters = list(stn_id[1:])
                        result_string = ''.join(list_of_characters)
                        #print(result_string)
                        # Retrieving stn_type and its location based on the station_id
                        cur = mydb.cursor()
                        query = f"SELECT stn_location, stn_type, stn_nm FROM stn_master WHERE stn_id = '{result_string}'"
                        cur.execute(query)
                        row = cur.fetchone()
                        print(row)
                        if row:
                            location, stn_type, stn_nm = row
                            # Convert date_time to datetime format
                            date_time = data[1]
                            datetime_obj = datetime.strptime(date_time, "%d/%m/%y %H:%M")
                            converted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M")
                            # Replace '--' with 0
                            sim_no = '0' if data[2] == '--' else data[2]
                            batt_vol = '0' if data[3] == '--' else data[3]
                            water_level = '0' if data[4] == '--' else data[4]
                            hr_rainfall = '0' if data[5] == '--' else data[5]
                            daily_rainfall = '0' if data[6] == '--' else data[6]
                            solar_vol = '0' if data[7] == '--' else data[7]
                            # print("datetime:", converted_datetime)
                            # print("sim_no:", sim_no)
                            # print("batt_vol:", batt_vol)
                            # print("water_level:", water_level)
                            # print("hr_rainfall:", hr_rainfall)
                            # print("daily_rainfall:", daily_rainfall)
                            # print("solar_voltage:", batt_vol)
                            query = "INSERT INTO realtime_data_query_table(stn_id,stn_location,stn_type,stn_nm,sim_no, datetime,water_level_value, hourly_rainfall_value, daily_rainfall_value, battery_voltage,solar_voltage) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                            try:
                                values = (
                                result_string, location, stn_type, stn_nm, sim_no, converted_datetime, water_level,
                                hr_rainfall, daily_rainfall, batt_vol, solar_vol)
                                # print(values)
                                cur.execute(query, values)
                                mydb.commit()
                                print(cur.rowcount, "row inserted")
                            except Exception as e:
                                print("Something went wrong:", e)
                        cur.close()
                    if len([column.strip() for column in data]) == 8 :  # Check if the row has 8 columns
                        result_string = data[0]
                        # Retrieving stn_type and its location based on the station_id
                        cur = mydb.cursor()
                        query = f"SELECT stn_location, stn_type, stn_nm FROM stn_master WHERE stn_id = '{result_string}'"
                        cur.execute(query)
                        row = cur.fetchone()
                        #print(row)
                        if row:
                            location, stn_type, stn_nm = row
                            # Convert date_time to datetime format
                            date_time = data[1]
                            date_part, time_part = date_time.split(' ')
                            print(f'date_time: {date_time}, date_part: {date_part}, time_part: {time_part}')

                            # Split the date into day, month, and year
                            day, month, year = date_part.split('-')

                            # Concatenate the components in the desired format
                            output_date = year + '-'+month + '-' + day + ' ' + time_part
                            # Replace '--' with 0
                            sim_no = '0' if data[2] == '--' else data[2]
                            batt_vol = '0' if data[3] == '--' else data[3]
                            water_level = '0' if data[4] == '--' else data[4]
                            hr_rainfall = '0' if data[5] == '--' else data[5]
                            daily_rainfall = '0' if data[6] == '--' else data[6]
                            solar_vol = batt_vol
                            # print("datetime:", converted_datetime)
                            # print("sim_no:", sim_no)
                            # print("batt_vol:", batt_vol)
                            # print("water_level:", water_level)
                            # print("hr_rainfall:", hr_rainfall)
                            # print("daily_rainfall:", daily_rainfall)
                            # print("solar_voltage:", batt_vol)
                            query = "INSERT INTO realtime_data_query_table(stn_id,stn_location,stn_type,stn_nm,sim_no, datetime,water_level_value, hourly_rainfall_value, daily_rainfall_value, battery_voltage,solar_voltage) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                            try:
                                values = (
                                result_string, location, stn_type, stn_nm, sim_no, output_date, water_level,
                                hr_rainfall, daily_rainfall, batt_vol, solar_vol)
                                cur.execute(query, values)
                                mydb.commit()
                                # print(cur.rowcount, "row inserted")
                            except Exception as e:
                                print("Something went wrong:", e)
                        cur.close()
                    if len([column.strip() for column in data]) == 8:  # Check if the row has 8 columns
                        stn_id = data[0]
                        list_of_characters = list(stn_id[1:])
                        result_string = ''.join(list_of_characters)
                        # Retrieving stn_type and its location based on the station_id
                        cur = mydb.cursor()
                        query = f"SELECT stn_location, stn_type, stn_nm FROM stn_master WHERE stn_id = '{result_string}'"
                        cur.execute(query)
                        row = cur.fetchone()
                        # print(row)
                        if row:
                            location, stn_type, stn_nm = row
                            # Convert date_time to datetime format
                            date_time = data[1]
                            date_part, time_part = date_time.split(' ')
                            print(f'date_time: {date_time}, date_part: {date_part}, time_part: {time_part}')

                            # Split the date into day, month, and year
                            if '/' in date_part:
                                day, month, year = date_part.split('/')
                            elif '-' in date_part:
                                day, month, year = date_part.split('-')
                            else:
                                # Handle the case where neither '/' nor '-' is present
                                print("Invalid date format")

                            # Concatenate the components in the desired format
                            output_date = year + '-' + month + '-' + day + ' ' + time_part
                            # Replace '--' with 0
                            sim_no = '0' if data[2] == '--' else data[2]
                            batt_vol = '0' if data[3] == '--' else data[3]
                            water_level = '0' if data[4] == '--' else data[4]
                            hr_rainfall = '0' if data[5] == '--' else data[5]
                            daily_rainfall = '0' if data[6] == '--' else data[6]
                            solar_vol = batt_vol
                            query = "INSERT INTO realtime_data_query_table(stn_id,stn_location,stn_type,stn_nm,sim_no, datetime,water_level_value, hourly_rainfall_value, daily_rainfall_value, battery_voltage,solar_voltage) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                            try:
                                values = (
                                    result_string, location, stn_type, stn_nm, sim_no, output_date, water_level,
                                    hr_rainfall, daily_rainfall, batt_vol, solar_vol)
                                cur.execute(query, values)
                                mydb.commit()
                                print(cur.rowcount, "row inserted")
                            except Exception as e:
                                print("Something went wrong:", e)
                        cur.close()
            # Move the processed file to the destination folder
            destination_file_path = os.path.join(destination_folder_path, csv_file)
            shutil.move(file_path, destination_file_path)

        time.sleep(120)

data_reading()


