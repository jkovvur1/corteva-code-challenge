-- The Data Doesn't mention to which data station the data belongs to. So, I am considering the file name as name of the data center as it is unique--

-- Weather_station table to store the name and unique id for a particular station. which will be referrenced in weather data

CREATE TABLE weather_station (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);


-- weather_data table holds the data of each in wx_data referrencing to the the weather station it belongs to and it also has a constraint (station_id, date) to 
--prevent duplication of data
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    station_id INTEGER NOT NULL REFERENCES weather_station(id),
    date DATE NOT NULL,
    max_temperature FLOAT,
    min_temperature FLOAT,
    precipitation FLOAT,
    CONSTRAINT unique_station_date UNIQUE (station_id, date)
);

