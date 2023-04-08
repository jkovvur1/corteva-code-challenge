import psycopg2
import glob
import os
from datetime import datetime

# Connect to PostgreSQL database
conn = psycopg2.connect("dbname=weatherdb user=postgres host='0.0.0.0' password=password")

# Variables to keep record of no of Records Ingested into the DB
weather_station_count = 0
weather_data_count = 0


print("Ingestion Started at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Loop through all files in wx_data directory
for file_path in glob.glob("../../wx_data/*.txt"):
    # Get station name from filename
    station_name = os.path.splitext(os.path.basename(file_path))[0].split(".")[0]

    # Read file and parse lines
    with open(file_path) as f:
        lines = f.readlines()

         # Insert record into database
        with conn.cursor() as cur:
            # Inserting weather station details
            cur.execute(f"INSERT INTO weather_station(name) VALUES ('{station_name}') ON CONFLICT DO NOTHING RETURNING id;")
            
            #fetching the generated Id for the weather station
            station_id = cur.fetchone()
            if station_id is None:
                break
            station_id = station_id[0]
            weather_station_count += 1

            for line in lines:
                # Parse data from line
                date_str, max_temp_str, min_temp_str, precip_str = line.strip().split("\t")
                date = datetime.strptime(date_str, "%Y%m%d").date()
                max_temp = float(max_temp_str) if max_temp_str != '-9999' else None
                min_temp = float(min_temp_str) if min_temp_str != '-9999' else None
                precip = float(precip_str) if precip_str != '-9999' else None
                    
                # Insert weather data of the station
                cur.execute("""
                    INSERT INTO weather_data (station_id, date, max_temperature, min_temperature, precipitation)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (station_id, date, max_temp, min_temp, precip))
            weather_data_count += len(lines)
            conn.commit()
            cur.close()

# Close database connection
conn.close()
print("Ingestion Completed at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("No of records Inserted into weather_station: " + str(weather_station_count))
print("No of Records Inserted into weather_data: " + str(weather_data_count))