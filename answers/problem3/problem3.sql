-- The weather_stats table contains the fields simiar to weather data to store the values for every year for every weather station

CREATE TABLE weather_stats (
  id SERIAL PRIMARY KEY,
  year INTEGER NOT NULL,
  station_id INTEGER NOT NULL REFERENCES weather_station(id),
  avg_max_temperature FLOAT,
  avg_min_temperature FLOAT,
  total_precipitation FLOAT
);

--The below query computes the 
-- * Average maximum temperature (in degrees Celsius)
-- * Average minimum temperature (in degrees Celsius)
-- * Total accumulated precipitation (in centimeters)
-- and store them in the above created table weather_stats

INSERT INTO weather_stats (year, station_id, avg_max_temperature, avg_min_temperature, total_precipitation)
SELECT
  EXTRACT(YEAR FROM date) AS year,
  station_id,
  AVG(max_temperature) /10.0 AS avg_max_temperature,
  AVG(min_temperature) /10.0 AS avg_min_temperature,
  SUM(precipitation) /100.0 AS total_precipitation
FROM
  weather_data
WHERE
  max_temperature <> -9999 AND
  min_temperature <> -9999 AND
  precipitation <> -9999
GROUP BY
  EXTRACT(YEAR FROM date),
  station_id;
