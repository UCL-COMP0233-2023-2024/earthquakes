# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests


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
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    ...

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return text

def count_earthquakes(data):
  string = requests.get(data).text
  lines = string.split('\n')
  return len(lines)

count_earthquakes('https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2000-01-01&maxlatitude=58.723&minlatitude=50.008&maxlongitude=1.67&minlongitude=-9.756&minmagnitude=1&endtime=2018-10-11&orderby=time-asc')

def create_lines(data):
  string = requests.get(data).text
  lines = string.split('\n')
  return lines

lines = create_lines('https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2000-01-01&maxlatitude=58.723&minlatitude=50.008&maxlongitude=1.67&minlongitude=-9.756&minmagnitude=1&endtime=2018-10-11&orderby=time-asc')
# lines

line = lines[1]
line = line[:-1]
line

import json

def get_magnitude(earthquake):
      """Retrive the magnitude of an earthquake item."""

      data = json.loads(earthquake)
      mag_value = data['properties']['mag']
      return mag_value

line = lines[5] # deciding the line
line = line[:-1] # cleaning up to get rid of last comma for error

get_magnitude(line)

def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""

    data = json.loads(earthquake)
    location = data['geometry']['coordinates'][:-1]
    return location


get_location(line)

def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    lines = data.split('\n')
    count = 0
    max_values = [0,[0,0]]
    for line in lines:
      if count == 0:
        line = line[359:-1]
        mag = get_magnitude(line)
        loc = get_location(line)
      elif count == 119:
        line = line[:-44]
        mag = get_magnitude(line)
        loc = get_location(line)
      else:
        line = line[:-1]
        mag = get_magnitude(line)
        loc = get_location(line)
      if max_values[0] < mag:
        max_values[0] = mag
        max_values[1] = loc
      count += 1

    return max_values[0],max_values[1]

get_maximum(data)