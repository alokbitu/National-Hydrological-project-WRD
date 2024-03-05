import mysql.connector
import time
from datetime import datetime

# Connect to the MySQL database
connection = mysql.connector.connect(host='localhost', user='root', password='admin', database='wrd_dash')

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

def get_last_update_time():
    try:
        with open("last_update_time.txt", "r") as file:
            return datetime.strptime(file.read().strip(), "%Y-%m-%d %H:%M:%S")
    except FileNotFoundError:
        return datetime(2000, 1, 1)  # Return an initial datetime if the file doesn't exist

def save_last_update_time(last_update_time):
    with open("last_update_time.txt", "w") as file:
        file.write(last_update_time.strftime("%Y-%m-%d %H:%M:%S"))

def copy_data(last_update_time):
    # Retrieve new data from the realtime_data_query_table with datetime greater than the last update time
    query = "SELECT * FROM realtime_data_query_table WHERE datetime > %s"
    cursor.execute(query, (last_update_time,))

    # Fetch all rows returned by the query
    rows = cursor.fetchall()

    # Update each row in the respective tables based on stn_type
    for row in rows:
        # Extract row data
        id_value = row[0]
        stn_id = row[1]
        stn_location = row[2]
        stn_type = row[3]
        stn_nm = row[4]
        sim_no = row[5]
        datetime_value = row[6]
        water_level_value = row[7]
        hourly_rainfall_value = row[8]
        daily_rainfall_value = row[9]
        battery_voltage = row[10]
        solar_voltage = row[11]

        # Perform the insertion into the respective tables based on stn_type
        if stn_type == "ARG":
            # Execute query for ARG stn_type
            arg_query = """
                INSERT INTO arg (stn_id, stn_type, stn_nm, location, hourly_rainfall, daily_rainfall, battery_voltage, solar_voltage, datetime)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(arg_query, (
                stn_id,
                stn_type,
                stn_nm,
                stn_location,
                hourly_rainfall_value,
                daily_rainfall_value,
                battery_voltage,
                solar_voltage,
                datetime_value
            ))
        elif stn_type == "AWL":
            # Execute query for AWL stn_type
            awl_query = """
                INSERT INTO awlr (stn_id, stn_type, stn_nm, location, water_level_value, battery_voltage, solar_voltage, datetime)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(awl_query, (
                stn_id,
                stn_type,
                stn_nm,
                stn_location,
                water_level_value,
                battery_voltage,
                solar_voltage,
                datetime_value
            ))
        elif stn_type == "ARG+AWL":
            # Execute query for ARG+AWL stn_type
            arg_awl_query = """
                INSERT INTO combine_station (stn_id, stn_type, stn_nm, location, hourly_rainfall_value, daily_rainfall_value, water_level_value, battery_voltage, solar_voltage, datetime)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(arg_awl_query, (
                stn_id,
                stn_type,
                stn_nm,
                stn_location,
                hourly_rainfall_value,
                daily_rainfall_value,
                water_level_value,
                battery_voltage,
                solar_voltage,
                datetime_value,
            ))

    # Commit the changes after processing all rows
    connection.commit()

    # Update the last update time with the current datetime_value, if there are rows processed
    if rows:
        last_update_time = rows[-1][6]  # The last row's datetime_value becomes the new last_update_time

    return last_update_time

def update_data(last_update_time):
    # Retrieve new data from the realtime_data_query_table with datetime greater than the last update time
    query = "SELECT * FROM realtime_data_query_table WHERE datetime > %s"
    cursor.execute(query, (last_update_time,))

    # Fetch all rows returned by the query
    rows = cursor.fetchall()

    # Update each row in the realtime_data_update_table
    for row in rows:
        # Extract row data
        id_value = row[0]
        stn_id = row[1]
        stn_location = row[2]
        stn_type = row[3]
        stn_nm = row[4]
        sim_no = row[5]
        datetime_value = row[6]
        water_level_value = row[7]
        hourly_rainfall_value = row[8]
        daily_rainfall_value = row[9]
        battery_voltage = row[10]
        solar_voltage = row[11]

        # Check if the stn_id already exists in realtime_data_update_table
        check_query = "SELECT COUNT(*) FROM realtime_data_update_table WHERE stn_id = %s"
        cursor.execute(check_query, (stn_id,))
        result = cursor.fetchone()

        if result[0] == 0:
            # Insert a new row if the stn_id doesn't exist in realtime_data_update_table
            insert_query = """
                INSERT INTO realtime_data_update_table (stn_id, stn_location, stn_type, sim_no, DATETIME, water_level_value, hourly_rainfall_value, daily_rainfall_value, battery_voltage, solar_voltage, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            cursor.execute(insert_query, (
                stn_id,
                stn_location,
                stn_type,
                sim_no,
                datetime_value,
                water_level_value,
                hourly_rainfall_value,
                daily_rainfall_value,
                battery_voltage,
                solar_voltage
            ))
        else:
            # Update the existing row if the stn_id already exists in realtime_data_update_table
            update_query = """
                UPDATE realtime_data_update_table
                SET
                    stn_location = %s,
                    stn_type = %s,
                    sim_no = %s,
                    DATETIME = %s,
                    water_level_value = %s,
                    hourly_rainfall_value = %s,
                    daily_rainfall_value = %s,
                    battery_voltage = %s,
                    solar_voltage = %s,
                    last_updated = NOW()
                WHERE stn_id = %s
            """
            cursor.execute(update_query, (
                stn_location,
                stn_type,
                sim_no,
                datetime_value,
                water_level_value,
                hourly_rainfall_value,
                daily_rainfall_value,
                battery_voltage,
                solar_voltage,
                stn_id
            ))

    # Commit the changes after processing all rows
    connection.commit()

    # Update the last update time with the current datetime_value, if there are rows processed
    if rows:
        last_update_time = rows[-1][6]  # The last row's datetime_value becomes the new last_update_time

    return last_update_time

if __name__ == '__main__':
    last_update_time_copy = get_last_update_time()  # Get the last saved datetime for copy_data()
    last_update_time_update = get_last_update_time()  # Get the last saved datetime for update_data()

    while True:
        try:
            last_update_time_copy = copy_data(last_update_time_copy)
            print("data get copied")
            last_update_time_update = update_data(last_update_time_update)
            print("data get updated")

            # Save the last update time to the text file after each iteration
            save_last_update_time(last_update_time_copy)

            time.sleep(60)
        except Exception as e:
            print("An error occurred:", str(e))
            break

    connection.close()
