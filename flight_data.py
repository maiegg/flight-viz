import requests
# import pytz

# KSAN bounding box
LON_MIN = -117.3
LON_MAX = -117.0
LAT_MIN = 32.6
LAT_MAX = 32.8

API_URL = f"https://opensky-network.org/api/states/all?lamin={LAT_MIN}&lomin={LON_MIN}&lamax={LAT_MAX}&lomax={LON_MAX}"

KSAN_COORD = (-117.1611, 32.7336)  # Longitude, Latitude for KSAN airport

# Fetch flights
def fetch_flights():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching flights: {e}")
        return None

def parse_flights(states):
    """ Extract (longitude, latitude, callsign, vertical_rate, on_ground) from state vectors """
    flights = []
    for state in states:
        if state[5] is not None and state[6] is not None:
            flight = {
                'lon': state[5],
                'lat': state[6],
                'callsign': (state[1] or '').strip(),
                'vertical_rate': state[11],
                'on_ground': state[8]
            }
            flights.append(flight)
    return flights

def categorize_flight(flight):
    """ Determine if flight is arriving, departing, or on ground """
    if flight['on_ground']:
        return 'ground'
    
    vertical_rate = flight.get('vertical_rate')
    if vertical_rate is not None:
        if vertical_rate < -1.5:
            return 'arriving'
        elif vertical_rate > 1.5:
            return 'departing'
    
    return 'unknown'
