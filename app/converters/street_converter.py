import geopy
from geopy.geocoders import Nominatim


def convert_street(lat, lon):
    locator = Nominatim(user_agent="myGeocoder")
    location: geopy.location.Location
    location = locator.reverse('{}, {}'.format(lat, lon), language='en', exactly_one=True)
    if 'city' in location.raw['address']:
        return location.raw['address']['city']
    else:
        raise AttributeError("make sure that you are in city or location which supports this functionality")
