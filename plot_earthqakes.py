from datetime import date
import matplotlib.pyplot as plt
import json
import requests
import numpy as np

def get_data():
    """Retrieve the data we will be working with."""
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
    return json.loads(text)


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
    return earthquake['properties']['mag']



# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    years = []
    
    for i in earthquakes:
        year = get_year(i)
        years.append(year)
        
    years = list(set(years))
    years.sort()
    
    dictionary_year = {}
    # dictionary["2017"] = [""]
    
    for year in years:
        mag1 = []
        for i in earthquakes:
            
            if get_year(i)==year:
                # dictionary_year[year] = i["properties"]["mag"]
                mag1.append(i["properties"]["mag"])
                dictionary_year[year] = mag1
        
    
    # year = get_year(earthquakes)
    return dictionary_year
    
    ...


def plot_average_magnitude_per_year(earthquakes):
    years_magnitude = get_magnitudes_per_year(earthquakes)
    for year in years_magnitude:
        mean_magnitude = np.mean(years_magnitude[year])
        years_magnitude[year] = mean_magnitude

    plt.plot(years_magnitude.keys(), years_magnitude.values())


    plt.show

def plot_number_per_year(earthquakes):
    years_magnitude = get_magnitudes_per_year(earthquakes)
    for year in years_magnitude:
        number_per_year = len(years_magnitude[year])
        years_magnitude[year] = number_per_year
    plt.plot(years_magnitude.keys(), years_magnitude.values())
    plt.show

# Get the data we will work with
quakes = get_data()['features']
# print(plot_average_magnitude_per_year(quakes))
# print(get_magnitudes_per_year(quakes))
# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_average_magnitude_per_year(quakes)

# plot_number_per_year(quakes)
# plt.legend("number")

