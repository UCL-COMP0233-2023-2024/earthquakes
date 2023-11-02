# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
from datetime import date

import matplotlib.pyplot as plt


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
    
    #with open('text.json', 'w') as json_file:

    #    json.dump(text, json_file, indent=4)

    #with open('text.json', 'r') as json_file:
    #    text_string = json_file.read()

    #print(text_string)

    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.

    # convert string to dictionary
    dic = json.loads(text)


    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    
    with open('dic.json', 'w') as json_file:

        json.dump(dic, json_file, indent=4)

    with open('dic.json', 'r') as json_file:
        dic_string = json_file.read()
    
    return dic

def count_earthquakes(data):
    
    return data["metadata"]["count"]


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]

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


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    mags_year = {}
    for i in data['features']:
        year = get_year(i)
        mag = get_magnitude(i)
        if year in mags_year:
            mags_year[year].append(mag)
        else:
            mags_year[year] = [mag]
            
    return mags_year

def plot_average_magnitude_per_year(earthquakes):
    # Calculate the average magnitudes per year
    mags_year = get_magnitudes_per_year(earthquakes)

    # Extract the years as 'x'
    x = list(mags_year.keys())
    
    # Create an empty list to store the calculated average magnitudes
    y = []

    # Calculate the average magnitude for each year and store it in 'y'
    for  year, magnitudes in mags_year.items():
        # Calculate the total magnitude for the year by summing up all magnitudes
        total_magnitude = sum(magnitudes)

        # Calculate the number of earthquakes for the year
        num_earthquakes = len(magnitudes)

        # Calculate the average magnitude for the year, but handle the case where there are no earthquakes (to avoid division by zero)
        if num_earthquakes > 0:
            average_magnitude = total_magnitude / num_earthquakes
        else:
            average_magnitude = 0

        # Append the calculated average magnitude to the 'y' list
        y.append(average_magnitude)

    # Print the items in the 'mags_year' dictionary
    print(mags_year.items())
    
    # Use plt.plot to create a line plot
    plt.plot(x, y)
    
    # Set the labels and title for the plot
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.title("Average Earthquake Magnitude Per Year")
    
    # Display the plot
    plt.show()

def plot_number_per_year(earthquakes):
    dict = get_magnitudes_per_year(data)
    x = list(dict.keys())

    y = []
    for i in dict:
        y.append(len(dict[i]))
    
    #print(x)
    #print(y)
    

    plt.bar(x,y)
    plt.xlabel('Years')
    plt.ylabel('Frequency')
    plt.title('Frequency of Earthquakes per year')
    plt.show()

def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake['geometry']['coordinates'][:2]


def get_maximum(data):
    max = 0
    location = 0 

    # Iterate through the earthquake data to find the earthquake with the maximum magnitude.
    for i in data['features']:
        if get_magnitude(i) > max:
            max = get_magnitude(i)
            location = get_location(i)

    # didn't account for multiple instances of the same maximum
    # initialise a list with earthquake, magnitude, earthquake magnitude, then save the values for all where it is a maximum as a list
    return max, location


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

new_dict = get_magnitudes_per_year(data)
#print(new_dict)

plot_number_per_year(data)

plot_average_magnitude_per_year(data)
