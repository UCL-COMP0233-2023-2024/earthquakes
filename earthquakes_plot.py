from datetime import date

import matplotlib.pyplot as plt
import requests
import json
import numpy as np


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
    return earthquake["properties"]["mag"]


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    year_dict={}
    for earth in earthquakes:
        if get_year(earth) in year_dict:
            year_dict[get_year(earth)].append(get_magnitude(earth))
        else:
            year_dict[get_year(earth)] = [get_magnitude(earth)]
    return year_dict


def plot_average_magnitude_per_year(earthquakes):
    dict = get_magnitudes_per_year(earthquakes)
    year_list =[]
    avg_list=[]
    for item in dict:
        year_list.append(item)

    year_list.sort()

    for year in year_list:
        mag_list = dict[year]
        value = 0
        for mag in mag_list:
            value += mag
        avg_list.append(value/len(mag_list))
    year_list=np.array(year_list)
    avg_list = np.array(avg_list)
    print(year_list,avg_list)
    plt.title('Average magnitude per year')
    plt.plot(year_list,avg_list, color='red')
    plt.xlabel('Year')
    plt.xticks(year_list,rotation=45)
    plt.ylabel('Average magnitude')
    plt.show()

def plot_number_per_year(earthquakes):
    ...


print(plot_average_magnitude_per_year(get_data()['features']))

# # Get the data we will work with
# quakes = get_data()['features']

# # Plot the results - this is not perfect since the x axis is shown as real
# # numbers rather than integers, which is what we would prefer!
# plot_number_per_year(quakes)
# plt.clf()  # This clears the figure, so that we don't overlay the two plots
# plot_average_magnitude_per_year(quakes)