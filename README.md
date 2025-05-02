# Real-time(ish) ADSB Logging 

+ `flight_data.py` contains calls to the API at https://opensky-network.org/ to retrieve all flights currently active within a bounding box
    + You must supply the boudning box; KSAN airport is used as an example
    + Attributes available for each flight: `icao24, callsign, origin_country, time_position, last_contact, longitude, latitude,
    baro_altitude, on_ground, velocity, heading, vertical_rate, sensors, geo_altitude, squawk, spi, position_source`
+ The API call is repeated periodically at a frequency of your choosing
+ Flights are categorized into (arrivals, departures, ground) based on the `on_ground` and `vertical_rate` attributes. 
    + Flight info is logged as JSON to 3 files, one for each category, in `logging/`
+ App.py sends these responses to a simple Flask application where they can be further displayed or mapped

Example result:
```
{
    'icao24': 'aa3f2e'
    , 'callsign': 'FLC76   '
    , 'origin_country': 'United States'
    , 'time_position': 1746052722
    , 'last_contact': 1746052722
    , 'longitude': -117.2167
    , 'latitude': 32.6934
    , 'baro_altitude': 144.78
    , 'on_ground': False
    , 'velocity': 70.26
    , 'heading': 193.12
    , 'vertical_rate': 8.13
    , 'sensors': None
    , 'geo_altitude': 129.54
    , 'squawk': '4757'
    , 'spi': False
    , 'position_source': 0
}
```

For retrieving larger batches of historical data, this project looks useful: https://github.com/adsblol/globe_history_2025, which archives global data, daily.

