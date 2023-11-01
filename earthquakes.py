from datetime import date

import matplotlib.pyplot as plt
import json
import requests
import itertools

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
    result = json.loads(text)
    return result


full_data = get_data()
earthquake_features = get_data()['features']


def get_year(earthquake):
    """Extract the year in which an earthquake happened"""
    timestamp = earthquake['properties']['time']
    year = date.fromtimestamp(timestamp/1000).year
    return year


    
    
def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    count = data['metadata']['count']
    return count

count_earthquakes(full_data)

def get_magnitude(result):
    """Retrieve the magnitude of an earthquake item."""
    magnitude = result['properties']['mag']
    #print(magnitude)
    return magnitude



def get_magnitudes_per_year(earthquakes):
    "Retrieve the magnitudes of all earthquakes in a given year"
    years = get_year(earthquakes)
    

years = []
magnitudes = []
locations = []

for earthquake in earthquake_features:
    magnitude = earthquake['properties']['mag']
    year = get_year(earthquake)
    location=earthquake['geometry']['coordinates'][:2]
    years.append(year)
    magnitudes.append(magnitude)
    locations.append(location)
    

mag_with_loc = list(zip(magnitudes,locations))


groupedBy = [(key, [num for _, num in value])
    for key, value in itertools.groupby(sorted(mag_with_loc), lambda x: x[0])]

print(groupedBy[-1])

max_mag_with_locations = groupedBy[-1]
max_magnitude, max_locations = max_mag_with_locations[0],max_mag_with_locations[1]
print(f"The strongest earthquakes were at locations {max_locations[0]} and {max_locations[1]} with magnitude {max_magnitude}")


earthquake_features = get_data()['features']
mag_with_loc = list(zip(magnitudes,locations))

#print(mag_with_loc)

#This is an alternative function that will find the maximum, preserving multiple maxima when present
#however this will not contain the location
def max_finder_with_duplicates(earthquake_features):
    max_mag = 0
    max_mag_vec = [max_mag]
    for earthquake in earthquake_features:
        magnitude = earthquake['properties']['mag']
        if magnitude>max_mag:  
            max_mag_vec.clear()
            max_mag_vec.append(magnitude)
            max_mag=magnitude
        elif magnitude == max_mag:
            for vec in max_mag_vec:
                if magnitude>vec:
                    max_mag_vec.remove(vec)
            max_mag_vec.append(magnitude)
            max_mag=magnitude
        print(max_mag_vec)    
    return max_mag_vec

#max_finder_with_duplicates(earthquake_features)

full_data = get_data()
earthquake_features = get_data()['features']


def get_year(earthquake):
    """Extract the year in which an earthquake happened"""
    timestamp = earthquake['properties']['time']
    year = date.fromtimestamp(timestamp/1000).year
    return year


years = []
magnitudes = []
locations = []

for earthquake in earthquake_features:
    magnitude = earthquake['properties']['mag']
    year = get_year(earthquake)
    location=earthquake['geometry']['coordinates'][:2]
    years.append(year)
    magnitudes.append(magnitude)
    locations.append(location)
    

mag_with_loc = list(zip(magnitudes,locations))

years_with_mag_with_loc = list(zip(years,magnitudes,locations))
#print(years_with_mag_with_loc)
    
years_with_mag = list(zip(years,magnitudes))

maxed = [(key, max(num for _, num in value))
    for key, value in itertools.groupby(years_with_mag, lambda x: x[0])]    



years_with_mag_with_loc = list(zip(years,magnitudes,locations))
    
years_with_mag = list(zip(years,magnitudes))

result = {}
for key, value in itertools.groupby(sorted(years_with_mag), lambda x: x[0]):
    values = list(num for _, num in value)
    result[key]=(sum(values)/len(values))

averaged = [(k, v) for k, v in result.items()]

print("\nAverage earthquake magnitude per year")
print(averaged)

x=[]
y=[]

for el in averaged:
    x.append(el[0])
    y.append(el[1])
    
#print(x,y)   
fig,ax = plt.subplots()
rects = ax.bar(x,y)
ax.set_xticks([ind for ind in x])
plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='center')
plt.legend(['Average magnitude per year'],loc=1, prop={'size': 6});
plt.show()

total = [(key, len(list(num for _, num in value)))
    for key, value in itertools.groupby(sorted(years_with_mag), lambda x: x[0])]

print("\nNumber of earthquakes per year")
print(total)

x2=[]
y2=[]

for el2 in total:
    x2.append(el2[0])
    y2.append(el2[1])
    
#print(x,y)   
fig2,ax2 = plt.subplots()
rects2 = ax2.bar(x2,y2)
ax2.set_xticks([ind for ind in x])
plt.setp(ax2.get_xticklabels(), rotation=30, horizontalalignment='center')
plt.legend(['Num of earthquakes per year'],loc=1, prop={'size': 6});
plt.show()