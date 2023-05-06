import json  # for saving dictionaries
from collections import defaultdict
import itertools
from tqdm import tqdm
import requests
import pymongo


# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ACS"]



# create variable lookup dictionary to be used later
VAR_URL = "https://api.census.gov/data/2021/acs/acsse/variables"
var_json = requests.get(VAR_URL).json()
lookup_2021 = {
    name: label
    for name, label, concept in var_json
    if name not in ("name", "for", "in", "ucgid")
}
lookup_2021['GEO_ID'] = 'GEO_ID'

concept_lookup_2021 = {
    name: concept
    for name, label, concept in var_json
    if name not in ("name", "for", "in", "ucgid")
}

vars_21 = list(lookup_2021.keys())


# generate data for 2021
HOST = "https://api.census.gov/data"
YEAR = "2021"

# http://mcdc.missouri.edu/applications/geocodes/?state=00
states = {
    "01": "Alabama",
    "02": "Alaska",
    "04": "Arizona",
    "05": "Arkansas",
    "06": "California",
    "08": "Colorado",
    "09": "Connecticut",
    "10": "Delaware",
    "11": "District of Columbia",
    "12": "Florida",
    "13": "Georgia",
    "15": "Hawaii",
    "16": "Idaho",
    "17": "Illinois",
    "18": "Indiana",
    "19": "Iowa",
    "20": "Kansas",
    "21": "Kentucky",
    "22": "Louisiana",
    "23": "Maine",
    "24": "Maryland",
    "25": "Massachusetts",
    "26": "Michigan",
    "27": "Minnesota",
    "28": "Mississippi",
    "29": "Missouri",
    "30": "Montana",
    "31": "Nebraska",
    "32": "Nevada",
    "33": "New Hampshire",
    "34": "New Jersey",
    "35": "New Mexico",
    "36": "New York",
    "37": "North Carolina",
    "38": "North Dakota",
    "39": "Ohio",
    "40": "Oklahoma",
    "41": "Oregon",
    "42": "Pennsylvania",
    "72": "Puerto Rico",
    "44": "Rhode Island",
    "45": "South Carolina",
    "46": "South Dakota",
    "47": "Tennessee",
    "48": "Texas",
    "49": "Utah",
    "50": "Vermont",
    "51": "Virginia",
    "53": "Washington",
    "54": "West Virginia",
    "55": "Wisconsin",
    "56": "Wyoming",
}

base_url = "/".join([HOST, YEAR, "acs/acsse"])

# group variables into correct category
grouped_vars = itertools.groupby(
    sorted(
        filter(
            lambda x: x.startswith('K'),
            vars_21
        )
    ),
    key=lambda x: x.split('_')[0]
)

grouped_vars = {key:list(group) for key, group in grouped_vars}

# add geo id to each category
for k, v in grouped_vars.items():
   v.append('GEO_ID')

def get_location_data_higher(level, location_name):
    predicates = {
        "key": "97d54f0b2bec96ce45749d21afa620949a6cd273",
        "for": f"{level}:*"
    }
    data_by_concept = defaultdict(list) # struct[concept] = collection; collection = [documents]
    for group, get_vars in grouped_vars.items():
        predicates["get"] = ",".join(get_vars)
        r = requests.get(base_url, params=predicates)
        if r.status_code != 200:
            print(f"Error retrieving data: {r.status_code}")
        
        names, *data = r.json()
        for da in data:
            d = dict(zip([lookup_2021.get(g,g) for g in names], da))
            data_by_concept[concept_lookup_2021[names[0]]].append(d)
    return data_by_concept

def get_location_data(location_ID, location_name):
    predicates = {
        "key": "97d54f0b2bec96ce45749d21afa620949a6cd273",
        "for": "county:*",
        "in": f"state:{location_ID}",
    }
    data_by_concept = defaultdict(list) # struct[concept] = collection; collection = [documents]
    for group, get_vars in grouped_vars.items():
        predicates["get"] = ",".join(get_vars)

        r = requests.get(base_url, params=predicates)
        if r.status_code != 200:
            print(f"Error retrieving data: {r.status_code}")
        
        names, *data = r.json()
        for da in data:
            d = dict(zip([lookup_2021.get(g,g) for g in names], da))
            data_by_concept[concept_lookup_2021[names[0]]].append(d)
    return data_by_concept

# work on higher level data
level_list = ["us", "region", "division", "state"]
for value in level_list:
    tqdm.write(f"Working on {value}")
    key_collections = get_location_data_higher(level=value, location_name=value)
    for k,v in key_collections.items():
        for i in v:
            if (i[str(next(iter(i)))]) != None:
                # cleanout i's values to be integers
                for tempkey in i:
                    if tempkey != 'GEO_ID':
                        try:
                            i[tempkey] = int(i[tempkey])
                        except: # median age by sex is float
                            i[tempkey] = float(i[tempkey])
                db[k].insert_one(i)

# county level
for key, value in states.items():
    tqdm.write(f"Working on {value}")
    key_collections = get_location_data(location_ID=key, location_name=value)
    for k,v in key_collections.items():
        for i in v:
            if (i[str(next(iter(i)))]) != None:
                # cleanout values to be integers
                for tempkey in i:
                    if tempkey != 'GEO_ID':
                        try:
                            i[tempkey] = int(i[tempkey])
                        except:
                            i[tempkey] = float(i[tempkey])
                db[k].insert_one(i)
