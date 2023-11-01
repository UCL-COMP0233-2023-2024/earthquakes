
# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # could also do response.json instead
    responseJson = json.loads(text)
    
    with open("response.json", "w") as file:
        json.dump(responseJson, file, indent=4)
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return responseJson


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data["metadata"]["count"]

def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]

def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake['geometry']['coordinates'][:2]

def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    # initiate maxMag and location
    location = 0
    maxMag = 0

    # iterate through the earthquakes to find the max magintude
    # should also have been able to handle earthquakes with the same mag
    for earthquake in data["features"]:
        if get_magnitude(earthquake) > maxMag:
            # assign the values to the variables
            maxMag = get_magnitude(earthquake)
            location = get_location(earthquake)
    return maxMag, location


# # With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

# The strongest earthquake was at [-2.15, 52.52] with magnitude 4.8














# create a dictionary where the keys are the years
# for each year, look at every eathquake
# if the year is equal then append the magnitude to the year 
