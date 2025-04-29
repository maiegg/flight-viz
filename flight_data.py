import requests
import logging
import time
# import pytz

# KSAN bounding box
LON_MIN = -117.3
LON_MAX = -117.0
LAT_MIN = 32.6
LAT_MAX = 32.8

API_URL = f"https://opensky-network.org/api/states/all?lamin={LAT_MIN}&lomin={LON_MIN}&lamax={LAT_MAX}&lomax={LON_MAX}"

KSAN_COORD = (-117.1611, 32.7336)  # Longitude, Latitude for KSAN airport

# Setup logging
logging.basicConfig(level=logging.INFO)
arrivals_logger = logging.getLogger('arrivals')
departures_logger = logging.getLogger('departures')
ground_logger = logging.getLogger('ground')

arrivals_handler = logging.FileHandler('logging/arrivals.log')
departures_handler = logging.FileHandler('logging/departures.log')
ground_handler = logging.FileHandler('logging/ground.log')

arrivals_logger.addHandler(arrivals_handler)
departures_logger.addHandler(departures_handler)
ground_logger.addHandler(ground_handler)

# Fetch flights
def fetch_flights():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Failed to fetch flights: {e}")
        return None
    
def categorize_flight(flight):
    icao24, callsign, origin_country, time_position, last_contact, longitude, latitude, \
    baro_altitude, on_ground, velocity, heading, vertical_rate, sensors, geo_altitude, \
    squawk, spi, position_source = flight

    if on_ground:
        return 'ground'
    
    if vertical_rate is not None:
        if vertical_rate < -1.5:
            return 'arriving'
        elif vertical_rate > 1.5:
            return 'departing'
    
    return None

def parse_flights(states):
    """ Extract (longitude, latitude, callsign, vertical_rate, on_ground) from state vectors """
    flights = []
    for flight in states:
        flight = dict(
            zip(
               ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'longitude', 'latitude',
                'baro_altitude', 'on_ground', 'velocity', 'heading', 'vertical_rate', 'sensors', 'geo_altitude',
                'squawk', 'spi', 'position_source'],
                flight
            )
        )

        if flight['vertical_rate'] is not None:
            if flight['vertical_rate'] < -1.5:
                arrivals_logger.info(f"{time.time()} - {flight}")
            elif flight['vertical_rate'] > 1.5:
                departures_logger.info(f"{time.time()} - {flight}")
            elif flight['on_ground']:
                ground_logger.info(f"{time.time()} - {flight}")
            
        if flight['latitude'] is not None and flight['longitude'] is not None:
            flights.append(flight)

    return flights