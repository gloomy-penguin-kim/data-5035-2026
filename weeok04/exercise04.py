import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


################################################################################################

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 38.94,
	"longitude": -92.33,
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "snowfall_sum", "rain_sum", "showers_sum", "wind_speed_10m_max", "wind_gusts_10m_max", "precipitation_hours"],
	"wind_speed_unit": "mph",
	"temperature_unit": "fahrenheit",
	"precipitation_unit": "inch",
	"start_date": "2025-12-31",
	"end_date": "2026-02-01",
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
daily_snowfall_sum = daily.Variables(5).ValuesAsNumpy()
daily_rain_sum = daily.Variables(6).ValuesAsNumpy()
daily_showers_sum = daily.Variables(7).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(8).ValuesAsNumpy()
daily_wind_gusts_10m_max = daily.Variables(9).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(10).ValuesAsNumpy()

daily_data =  {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["source"] = "University of Missouri - Columbia"
daily_data["enrollment"] = 27970 
daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
daily_data["snowfall_sum"] = daily_snowfall_sum
daily_data["rain_sum"] = daily_rain_sum
daily_data["showers_sum"] = daily_showers_sum
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max 

daily_dataframe1 = pd.DataFrame(data = daily_data)


################################################################################################


# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 37.20,
	"longitude": -93.28,
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "snowfall_sum", "rain_sum", "showers_sum", "wind_speed_10m_max", "wind_gusts_10m_max", "precipitation_hours"],
	"wind_speed_unit": "mph",
	"temperature_unit": "fahrenheit",
	"precipitation_unit": "inch",
	"start_date": "2025-12-31",
	"end_date": "2026-02-01",
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
daily_snowfall_sum = daily.Variables(5).ValuesAsNumpy()
daily_rain_sum = daily.Variables(6).ValuesAsNumpy()
daily_showers_sum = daily.Variables(7).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(8).ValuesAsNumpy()
daily_wind_gusts_10m_max = daily.Variables(9).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(10).ValuesAsNumpy()

daily_data =  {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["source"] = "Missouri State University - Springfield"
daily_data["enrollment"] = 27235 
daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
daily_data["snowfall_sum"] = daily_snowfall_sum
daily_data["rain_sum"] = daily_rain_sum
daily_data["showers_sum"] = daily_showers_sum
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max 

daily_dataframe2 = pd.DataFrame(data = daily_data)


################################################################################################


# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 38.79,
	"longitude": -90.50,
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "snowfall_sum", "rain_sum", "showers_sum", "wind_speed_10m_max", "wind_gusts_10m_max", "precipitation_hours"],
	"wind_speed_unit": "mph",
	"temperature_unit": "fahrenheit",
	"precipitation_unit": "inch",
	"start_date": "2025-12-31",
	"end_date": "2026-02-01",
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
daily_snowfall_sum = daily.Variables(5).ValuesAsNumpy()
daily_rain_sum = daily.Variables(6).ValuesAsNumpy()
daily_showers_sum = daily.Variables(7).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(8).ValuesAsNumpy()
daily_wind_gusts_10m_max = daily.Variables(9).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(10).ValuesAsNumpy()

daily_data =  {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["source"] = "Lindenwood University"
daily_data["enrollment"] = 7288 
daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
daily_data["snowfall_sum"] = daily_snowfall_sum
daily_data["rain_sum"] = daily_rain_sum
daily_data["showers_sum"] = daily_showers_sum
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max 

daily_dataframe3 = pd.DataFrame(data = daily_data)


################################################################################################


# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 37.31,
	"longitude": -89.53,
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "snowfall_sum", "rain_sum", "showers_sum", "wind_speed_10m_max", "wind_gusts_10m_max", "precipitation_hours"],
	"wind_speed_unit": "mph",
	"temperature_unit": "fahrenheit",
	"precipitation_unit": "inch",
	"start_date": "2025-12-31",
	"end_date": "2026-02-01",
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
daily_snowfall_sum = daily.Variables(5).ValuesAsNumpy()
daily_rain_sum = daily.Variables(6).ValuesAsNumpy()
daily_showers_sum = daily.Variables(7).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(8).ValuesAsNumpy()
daily_wind_gusts_10m_max = daily.Variables(9).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(10).ValuesAsNumpy()

daily_data =  {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["source"] = "Southeast Missouri State University -SEMO"
daily_data["enrollment"] = 9500
daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
daily_data["snowfall_sum"] = daily_snowfall_sum
daily_data["rain_sum"] = daily_rain_sum
daily_data["showers_sum"] = daily_showers_sum
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max 

daily_dataframe4 = pd.DataFrame(data = daily_data)


################################################################################################

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 39.0333,
	"longitude": -94.58,
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "snowfall_sum", "rain_sum", "showers_sum", "wind_speed_10m_max", "wind_gusts_10m_max", "precipitation_hours"],
	"wind_speed_unit": "mph",
	"temperature_unit": "fahrenheit",
	"precipitation_unit": "inch",
	"start_date": "2025-12-31",
	"end_date": "2026-02-01",
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
daily_snowfall_sum = daily.Variables(5).ValuesAsNumpy()
daily_rain_sum = daily.Variables(6).ValuesAsNumpy()
daily_showers_sum = daily.Variables(7).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(8).ValuesAsNumpy()
daily_wind_gusts_10m_max = daily.Variables(9).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(10).ValuesAsNumpy()

daily_data =  {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["source"] = "University of Missouri - KC"
daily_data["enrollment"] = 14904 
daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
daily_data["snowfall_sum"] = daily_snowfall_sum
daily_data["rain_sum"] = daily_rain_sum
daily_data["showers_sum"] = daily_showers_sum
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max 

daily_dataframe5 = pd.DataFrame(data = daily_data)


################################################################################################

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 38.6359,
	"longitude": -90.2341,
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "snowfall_sum", "rain_sum", "showers_sum", "wind_speed_10m_max", "wind_gusts_10m_max", "precipitation_hours"],
	"wind_speed_unit": "mph",
	"temperature_unit": "fahrenheit",
	"precipitation_unit": "inch",
	"start_date": "2025-12-31",
	"end_date": "2026-02-01",
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
daily_snowfall_sum = daily.Variables(5).ValuesAsNumpy()
daily_rain_sum = daily.Variables(6).ValuesAsNumpy()
daily_showers_sum = daily.Variables(7).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(8).ValuesAsNumpy()
daily_wind_gusts_10m_max = daily.Variables(9).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(10).ValuesAsNumpy()

daily_data =  {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["source"] = "Saint Louis University - SLU"
daily_data["enrollment"] = 17082  
daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
daily_data["snowfall_sum"] = daily_snowfall_sum
daily_data["rain_sum"] = daily_rain_sum
daily_data["showers_sum"] = daily_showers_sum
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max 

daily_dataframe6 = pd.DataFrame(data = daily_data)


################################################################################################
 
pd_df = pd.concat([daily_dataframe1, 
                   daily_dataframe2, 
                   daily_dataframe3, 
                   daily_dataframe4, 
                   daily_dataframe5, 
                   daily_dataframe6]) 

spark_df = spark.createDataFrame(pd_df)

spark_df.createOrReplaceTempView("january_data")
 
# formatted with https://www.dpriver.com/pp/sqlformat.htm
# commented with the help of ChatGPT 5.2 and Databricks AI SQL assistant

result_df = spark.sql("""
-- ============================================================
--
-- NCAA Division I Football Team Universities in Missouri 
--
-- Final aggregation: One row per university
-- Calculates number of severe-weather days and student-days
-- impacted based on your chosen definitions.
-- ============================================================

SELECT
    university,
    "MO" as state, 
    enrollment,

    -- Count of school days where average temp < freezing
    SUM(freezing_day) AS freezing_days,

    -- Student-days impacted by freezing temps
    -- (enrollment * number of freezing days)
    SUM(freezing_day) * enrollment AS enrollment_freezing_days,

    -- Count of days with snowfall OR snowfall the day before
    SUM(snow_day_or_before) AS snow_days,

    -- Student-days impacted by snow conditions
    SUM(snow_day_or_before) * enrollment AS enrollment_snow_day_or_before,

    -- Count of days with rain while below freezing
    -- (proxy for freezing rain / dangerous conditions)
    SUM(freezing_rain_day) AS freezing_rain_days,

    -- Student-days impacted by freezing rain
    SUM(freezing_rain_day) * enrollment AS enrollment_freezing_rain_day,

    -- List of student-days impacted by severe weather
    collect_list(
        CASE WHEN y.freezing_day = 1 or y.snow_day_or_before = 1  or y.freezing_day = 1 THEN date_format(date, "MM-dd") END
    ) AS severe_days_list 

FROM (

    -- ========================================================
    -- Create daily flags indicating severe weather conditions
    -- ========================================================
    SELECT
        source AS university,
        enrollment,
        date,

        -- Flag if the school day was below freezing
        CASE
            WHEN below_freezing_school_day
                 OR below_freezing_school_day_apparent
            THEN 1
            ELSE 0
        END AS freezing_day,

        -- Flag if snow occurred today or yesterday
        -- (captures lingering disruption)
        CASE
            WHEN db4_snowfall_inches > 0
                 OR snowfall_inches > 0
            THEN 1
            ELSE 0
        END AS snow_day_or_before,

        -- Flag freezing rain condition
        -- Rain combined with freezing temperatures
        CASE
            WHEN rain_inches > 0
                 AND (
                     below_freezing_school_day
                     OR below_freezing_school_day_apparent
                 )
            THEN 1
            ELSE 0
        END AS freezing_rain_day

    FROM (

        -- ====================================================
        -- Join weather data with previous day snowfall
        -- Also compute freezing temperature indicators
        -- ====================================================
        SELECT
            j.source,
            j.date,
            j.enrollment,

            -- Day-of-week used to filter to school days
            DATE_FORMAT(j.date, 'E') AS dow,

            -- Real temperature freezing check
            (j.temperature_2m_max + j.temperature_2m_min) / 2 < 32.0
                AS below_freezing_school_day,

            -- Apparent temperature freezing check
            (j.apparent_temperature_max + j.apparent_temperature_min) / 2 < 32.0
                AS below_freezing_school_day_apparent,

            -- Snow yesterday
            dayb4.snowfall_sum AS db4_snowfall_inches,

            -- Snow today
            j.snowfall_sum AS snowfall_inches,

            -- Rain today
            j.rain_sum AS rain_inches

        FROM january_data AS j

        -- Join previous day's weather to capture lingering effects
        LEFT OUTER JOIN january_data AS dayb4
            ON j.date = DATE_ADD(dayb4.date, -1)
            AND dayb4.source = j.source

        -- Only count weekdays (school days)
        WHERE DATE_FORMAT(j.date, 'E') IN ('Mon','Tue','Wed','Thu','Fri')

        -- Restrict to January 2026 period
        AND j.date >= '2026-01-01'

    ) AS x

) AS y

-- Final aggregation grain: one row per university
GROUP BY
    university,
    enrollment

ORDER BY
    university,
    enrollment;

                    """) 

result_df.show(truncate=False) 
 
