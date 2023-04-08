CREATE TABLE weather_stats (
  id SERIAL PRIMARY KEY,
  year INTEGER NOT NULL,
  station_id INTEGER NOT NULL REFERENCES weather_station(id),
  avg_max_temperature FLOAT,
  avg_min_temperature FLOAT,
  total_precipitation FLOAT
);


INSERT INTO weather_stats (year, station_id, avg_max_temperature, avg_min_temperature, total_precipitation)
SELECT
  EXTRACT(YEAR FROM date) AS year,
  station_id,
  AVG(max_temperature) AS avg_max_temperature,
  AVG(min_temperature) AS avg_min_temperature,
  SUM(precipitation) AS total_precipitation
FROM
  weather_data
WHERE
  max_temperature <> -9999 AND
  min_temperature <> -9999 AND
  precipitation <> -9999
GROUP BY
  EXTRACT(YEAR FROM date),
  station_id;
