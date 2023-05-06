To build them run:
python3 acs.py
python3 redistricting.py


Both ACS and Redistricting now have GEO_ID; however this isn't the same as the s2 cells in influxdb.
Potentially Travis's geojson script might be helpful in converting between the two, but I have not looked into it
https://github.com/travisdula/us-census-2018-geojson

Mongosh might also have to installed, but not sure if it is already


These are the different parameters to query/narrow down for locations:
us
region
division
state
county
GEO_ID

These are the Redistricting data only parameters:
"county subdivision"
tract   # currently the API seems to not have data at purely at the tract level, but there is data at lower levels, so could be compiled from the track-block_group level if needed
"block group"
block
"congressional district"
"voting district"
place



example query to get the block_groups in county 13 of state 2 (Alaska)  (this format is using the mongodb gui)
{tract: {$exists: true}, block: {$exists: false}, county: 13, state: 2}

You can use Mongosh to run the same queries through the terminal:
use Redistricting (this puts you on the correct database)
db.RACE.find({tract: {$exists: true}, block: {$exists: false}, county: 13, state: 2})

#python script to do the same thing, example is from the redistricting database, querying in the 'Race' collection, which also has the total population
include pymongo
client = MongoClient('mongodb://localhost:27017/')
filter={
    'tract': {
        '$exists': True
    }, 
    'block': {
        '$exists': False
    }, 
    'county': 13, 
    'state': 2
}
result = client['Redistricting']['RACE'].find(
  filter=filter
)