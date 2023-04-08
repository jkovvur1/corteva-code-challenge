# Run Usisng uvicorn main:app --reload

import psycopg2
from fastapi import FastAPI
from typing import Optional

# Creating FAST API instance
app = FastAPI()


def get_connection():
    '''
    Method to get database connection
    '''
    conn = psycopg2.connect(
    host="0.0.0.0",
    database="weatherdb",
    user="postgres",
    password="password")
    return conn

@app.get("/api/weather")
async def get_weather_data(station_id: Optional[int] = None, date: Optional[str] = None, page: Optional[int] = 1, limit: Optional[int] = 100):
    offset = (page - 1) * limit
    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT * FROM weather_data"
    conditions = []
    params = []
    # checking query params
    if station_id is not None:
        conditions.append("station_id = %s")
        params.append(station_id)
    if date is not None:
        conditions.append("date = %s")
        params.append(date)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += f" OFFSET {offset} LIMIT {limit}"

    cur.execute(query, params)
    rows = cur.fetchall()
    result = []
    # forming response
    for row in rows:
        result.append({"station_id":row[1],
                       "date": row[2].strftime("%Y-%m-%d"), 
                       "max_temperature": row[3], 
                       "min_temperature": row[4], 
                       "precipitation": row[5]})
    cur.close()
    conn.close()
    return result

@app.get("/api/weather/stats")
async def get_weather_stats(station_id: Optional[int] = None, page: Optional[int] = 1, limit: Optional[int] = 100):
    offset = (page - 1) * limit
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT weather_data.station_id, weather_station.name, extract(year from weather_data.date), avg(weather_data.max_temperature/10.0), avg(weather_data.min_temperature/10.0), sum(weather_data.precipitation/10.0)/10.0 FROM weather_data JOIN weather_station ON weather_data.station_id = weather_station.id"
    #checking query params
    if station_id is not None:
        query += f" WHERE weather_data.station_id={station_id}"
    query += " GROUP BY weather_data.station_id, weather_station.name, extract(year from weather_data.date)"
    query += f" OFFSET {offset} LIMIT {limit};"
    cur.execute(query)
    rows = cur.fetchall()
    result = []
    #forming response
    for row in rows:
        data = {
            "station_id": row[0],
            "station_name": row[1],
            "year": int(row[2]),
            "avg_max_temperature": row[3],
            "avg_min_temperature": row[4],
            "total_precipitation": row[5]
        }
        result.append(data)
    cur.close()
    conn.close()
    return result
