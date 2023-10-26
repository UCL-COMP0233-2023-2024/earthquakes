from datetime import date
import matplotlib.pyplot as plt
import json
import numpy as np


def get_data():
    """Retrieve the data we will be working with."""
    text = open('Earthquake.json', 'r')
    data = text.read()
    text.close()
    return json.loads(data)



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
    data = {}

    for earthquake in earthquakes:
        year = get_year(earthquake)
        magnitude = get_magnitude(earthquake)

        if year not in data:
            data[year] = []

        data[year].append(magnitude)
    
    return data


def plot_average_magnitude_per_year(earthquakes):
    data = get_magnitudes_per_year(earthquakes)
    years = []
    avgnum_per_year = []

    for year in data:
        years.append(year)
        avgnum_per_year.append(np.mean(data[year]))

    plt.plot(years, avgnum_per_year)
    plt.title("Average magnitude per year.")
    for a, b in zip(years, avgnum_per_year):
        plt.text(a, b, '%.3f' % b, ha = 'center', va = 'bottom', fontsize = 10)
    plt.xticks(years, rotation = 45)
    plt.show()


def plot_number_per_year(earthquakes):
    data = get_magnitudes_per_year(earthquakes)
    years = []
    num_per_year = []

    for year in data:
        years.append(year)
        num_per_year.append(len(data[year]))

    plt.plot(years, num_per_year)
    plt.title("Number of earthquakes per year.")
    for a, b in zip(years, num_per_year):
        plt.text(a, b, '%.3f' % b, ha = 'center', va = 'bottom', fontsize = 10)
    plt.xticks(years, rotation = 45)
    plt.show()



# Get the data we will work with
quakes = get_data()['features']
# print(quakes)

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
