import json  # for saving dictionaries
from collections import defaultdict
import itertools
from tqdm import tqdm
import numpy as np
import requests
import pymongo


# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Redistricting"]


# create variable lookup dictionary to be used later
VAR_URL = "https://api.census.gov/data/2020/dec/pl/variables"
var_json = requests.get(VAR_URL).json()
lookup_2020 = {
    name: label
    for name, label, concept in var_json
    if name not in ("name", "for", "in", "ucgid")
}
lookup_2020['GEO_ID'] = 'GEO_ID'

# the keys have spaces at the beginning, so get rid of extra spaces
for k, v in lookup_2020.items():
        lookup_2020[k] = v.lstrip()

concept_lookup_2020 = {
    name: concept
    for name, label, concept in var_json
    if name not in ("name", "for", "in", "ucgid")
}

vars_20 = list(lookup_2020.keys())

HOST = "https://api.census.gov/data"
YEAR = "2020"

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

base_url = "/".join([HOST, YEAR, "dec/pl"])

grouped_vars = itertools.groupby(
    sorted(
        filter(
            lambda x: x.startswith('P1') or x.startswith('P2') or x.startswith('P3') or x.startswith('P3') or x.startswith('P4') or x.startswith('P5') or x.startswith('H1'),
            vars_20
        )
    ),
    key=lambda x: x.split('_')[0]
)

grouped_vars = {key:list(group) for key, group in grouped_vars}

# add geo_id to each category
for k, v in grouped_vars.items():
   v.append('GEO_ID')

def get_location_data_higher(level, location_name):
    predicates = {
        "key": "97d54f0b2bec96ce45749d21afa620949a6cd273",
        "for": f"{level}:*"
    }
    data_by_concept = defaultdict(list)
    for group, get_vars_grouped in grouped_vars.items():
        #slice it into smaller parts 
        N = len(get_vars_grouped)
        slices = list(np.arange(0, N, 40))
        slices.append(N-1)
        
        #setup to append them
        names = list()
        data = list()
        data.append(list())
        for i in range(1, len(slices)):
            addme = 1
            if i == 1:
                addme = 0
            get_vars = get_vars_grouped[slices[i-1] + addme:slices[i] + 1]
            predicates["get"] = ",".join(get_vars)
            try:
                r = requests.get(base_url, params=predicates)
                if r.status_code != 200 and r.status_code != 400:
                    print(f"Error retrieving data: {r.status_code}")
                
                #add the nested data to the data
                namestemp, *datatemp = r.json()
                if len(names) == 0:
                    data = datatemp
                    names = namestemp
                else:
                    for i in range(len(datatemp)):
                        data[i] = (data[i])[:(len(data[i]) - 1)] + datatemp[i]
                    names = names[:(len(names) - 1)] + namestemp
            except requests.exceptions.Timeout:
                print("TimeoutError: skipping")
            except:
                pass

        if len(names) > 0:
            for da in data:
                d = dict(zip([lookup_2020.get(g,g) for g in names], da))
                data_by_concept[concept_lookup_2020[names[0]]].append(d)
    return data_by_concept

def get_location_data(location_ID, location_name, p):
    predicates = {
        "key": "97d54f0b2bec96ce45749d21afa620949a6cd273",
        "for": p[1],
        "in": p[2].format(location_ID) if "state:{}" in p[2] else p[2],
    }
    data_by_concept = defaultdict(list)
    
    for group, get_vars_grouped in grouped_vars.items():
        #slice it into smaller parts, since the Census API won't allow for too many predicates
        N = len(get_vars_grouped)
        slices = list(np.arange(0, N, 40))
        slices.append(N-1)
        
        #setup to append them
        names = list()
        data = list()
        data.append(list())
        for i in range(1, len(slices)):
            addme = 1
            if i == 1:
                addme = 0
            get_vars = get_vars_grouped[slices[i-1] + addme:slices[i] + 1]
            predicates["get"] = ",".join(get_vars)
            try:
                r = requests.get(base_url, params=predicates)
                if r.status_code != 200 and r.status_code != 400:
                    print(f"Error retrieving data: {r.status_code}")
                
                #add the nested data to the data
                namestemp, *datatemp = r.json()
                if len(names) == 0:
                    data = datatemp
                    names = namestemp
                else:
                    numIdentifiers = len(names) - 41
                    for i in range(len(datatemp)):
                        data[i] = (data[i])[:(len(data[i]) - numIdentifiers)] + datatemp[i]
                    names = names[:(len(names) - numIdentifiers)] + namestemp
            except requests.exceptions.Timeout:
                print("TimeoutError: skipping")
            except:
                pass
        
        if len(names) > 0:
            for da in data:
                d = dict(zip([lookup_2020.get(g,g) for g in names], da))
                data_by_concept[concept_lookup_2020[names[0]]].append(d)
    return data_by_concept

# work on higher level data
level_list = ["us", "region", "division", "state"]
for value in level_list:
    tqdm.write(f"Working on {value}")
    key_collections = get_location_data_higher(level=value, location_name=value)
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



# each key has a tuple: (name, for, in)
predicates = {
    "050": ("state-county", "county:*", "state:{}"),
    "060": ("state-county-county_subdivision", "county subdivision:*", "state:{}"),
    "100": ("state-county-tract-block", "block:*", "state:{};county:*"),
    #"140": ("state-county-tract", "tract:*", "state:{};county:*;"), #currently seems to not have data at tract level, could be compiled from the track-block_group level if needed
    "150": ("state-county-tract-block_group", "block group:*", "state:{};county:*;tract:*"), 
    "160": ("state-place", "place:*", "state:{}"),
    "500": ("state-congressional_district", "congressional district:*", "state:{}"),
    "700": ("state-county-voting_district", "voting district:*", "state:{};county:*"),
}

for a, p in predicates.items():
    tqdm.write(f"\n\nWORKING ON THE {p[0]} level")
    for key, value in states.items():
        tqdm.write(f"Working on {value}")
        key_collections = get_location_data(location_ID=key, location_name=value, p=p)
        for k,v in key_collections.items():
            for i in v:
                if (i[str(next(iter(i)))]) != None:
                    # cleanout values to be integers
                    for tempkey in i:
                        if tempkey != 'GEO_ID':
                            try:
                                i[tempkey] = int(i[tempkey])
                            except: # some of the voting districts have bad formatting 
                                pass
                    db[k].insert_one(i)