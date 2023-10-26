from datetime import date
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_data():
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
    text = response.text
    dict_text = json.loads(text)  # change it to dictionary type
    return dict_text


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['mag']


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    result = {}
    for i in earthquakes:
        year = get_year(i)
        mag = get_magnitude(i["properties"])
        if year in result.keys():
            result[year].append(mag)
        else:
            result[year] = [mag]
    return result


def plot_average_magnitude_per_year(earthquakes):
    mag_data = get_magnitudes_per_year(earthquakes)
    list_data = {}
    for i in mag_data.keys():
        list_data[i] = np.average(mag_data[i])
    #print(list_data)
    plt.plot(list(list_data.keys()), list(list_data.values()))
    plt.xticks(list(list_data.keys()), rotation = 45)
    plt.show()


def plot_number_per_year(earthquakes):
    mag_data = get_magnitudes_per_year(earthquakes)
    list_data = {}
    for i in mag_data.keys():
        list_data[i] = len(mag_data[i])
    plt.plot(list(list_data.keys()), list(list_data.values()))
    plt.xticks(list(list_data.keys()), rotation = 45)
    plt.show()




# Get the data we will work with
quakes = get_data()['features']
#for i in range(1):
#    print(quakes[i])
# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
