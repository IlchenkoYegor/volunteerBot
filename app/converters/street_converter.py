#%load_ext autotime
import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import plotly_express as px
import tqdm
from tqdm._tqdm_notebook import tqdm_notebook


def convert_street(lat, lon):
    locator = Nominatim(user_agent="myGeocoder")
    location: geopy.location.Location
    location = locator.reverse('{}, {}'.format(lat, lon), language='en', exactly_one=True)
    print(location.raw)
    if 'city' in location.raw['address']:
        return location.raw['address']['city']
    else:
        raise AttributeError("make sure that you are in city or location which supports this functionality")





#from prev prj
    # if 'city' in location.raw['address']:
    #     return location.raw['address']['city']+', '+location.raw['address']['road'], location.raw['address']['state']
    # elif 'village' in location.raw['address'] and 'road' in location.raw['address']:
    #     return location.raw['address']['village'] + ', ' + location.raw['address']['road'], location.raw['address']['state']
    # elif 'county' in location.raw['address']:
    #     return location.raw['address']['county']+', '+ location.raw['address']['village'], location.raw['address']['state']
    # elif 'village' in location.raw['address']:
    #     return location.raw['address']['village'], location.raw['address']['state']
    # elif('municipality' in location.raw['address']) :
    #     return location.raw['address']['municipality'], location.raw['address']['state']
    # else:
    #     return location.raw['address']['country'], location.raw['address']['state']